# Simple random graphs with constrained endpoint pairs

Repository: https://github.com/Qiskit/rustworkx

Repair `gnm_random_graph` so undirected graphs contain exactly the requested distinct non-loop edges (or the complete graph when m exceeds capacity). Preserve the existing directed API, reproducibility and generic graph support.

Also export `generators::gnm_random_graph_with_forbidden_edges` with arguments `(num_nodes: usize, num_edges: usize, seed: Option<u64>, forbidden_edges: &[(usize, usize)], default_node_weight: F, default_edge_weight: H) -> Result<G, InvalidInputError>`, with the same generic Build/Create/Data/NodeIndexable conventions as the existing generator.

The new generator must produce exactly m uniformly sampled distinct allowed non-loop edges. Forbidden pairs use zero-based endpoint indices; undirected reverse pairs are equivalent, directed reverse pairs are distinct, and repeated forbidden pairs are deduplicated. n=0, invalid endpoints, forbidden loops, edge-space overflow beyond usize, and m greater than the allowed capacity return InvalidInputError before calling either weight callback. n=1,m=0 is valid. For valid requests, call the node callback exactly n times and the edge callback exactly m times; callback values must become the actual graph weights.

Same inputs and seed must yield identical edge order and weights independently of HashSet iteration. Do not enumerate or allocate the full quadratic edge space for sparse requests. For n=50,000,m=200 the generator must remain practical; near saturation it should sample the complement rather than retry almost indefinitely. Support petgraph Graph and StableGraph in directed and undirected modes, without assuming node identifiers are integers. Keep existing random-generator regressions passing. No exact legacy seeded edge order is required for the new API.

## Stateful sampling for incremental graph construction

Also export `generators::GnmEdgeSampler`, implementing `Clone` and the methods `new(n: usize, directed: bool, seed: Option<u64>, forbidden: &[(usize,usize)]) -> Result<Self,InvalidInputError>`, `available(&self) -> usize`, `take(&mut self, count: usize) -> Result<Vec<(usize,usize)>,InvalidInputError>`, and `release(&mut self, edges: &[(usize,usize)]) -> Result<(),InvalidInputError>`.

It leases distinct uniform allowed non-loop endpoint pairs without constructing a graph. `take` returns draw order, and `take(a)` followed by `take(b)` has the same ordered output and future RNG state as `take(a+b)`. Undirected outputs are canonical `(min,max)`; exclusions are canonicalized and deduplicated. Directed reversed pairs remain distinct. Seeded output cannot depend on exclusion order or duplicates. A clone is an independent snapshot, including RNG and outstanding leases.

Infeasible take, invalid construction, and invalid release return InvalidInputError. A release accepts only distinct currently leased pairs (undirected reverse accepted), rejecting duplicate/reversed duplicates, loops, out-of-range, forbidden, and already released pairs. Failed take/release must leave both availability and future sampled stream unchanged. Empty operations succeed without advancing RNG. Successful release makes those pairs available again. Exhaustion terminates without rejection loops; it is valid to drain, release, and drain repeatedly.

This is a reusable incremental sampler: avoid quadratic edge-space storage, and avoid work linear in the entire history on every draw. Sparse n=100,000 batches totaling 50,000 edges, followed by release/redraw, and many small drains near saturation must remain practical under normal Rust debug builds. Storage should remain proportional to distinct forbidden pairs plus current outstanding leases, rather than accumulating every historical draw or one allocation per possible edge. No exact choice of PRNG or legacy seeded ordering is required; the observable batching, uniformity, canonicalization and atomicity rules are required. Preserve the one-shot constrained and existing generator APIs.

## Restricted draws and changing graph size

Extend the same GnmEdgeSampler with `available_between(&self, left: &[usize], right: &[usize]) -> Result<usize, InvalidInputError>`, `take_between(&mut self, left: &[usize], right: &[usize], count: usize) -> Result<Vec<(usize,usize)>,InvalidInputError>`, and `reconfigure(&mut self, n: usize, forbidden: &[(usize,usize)]) -> Result<(),InvalidInputError>`.

The two vertex lists select a bipartite view of the live pool. Normalize each to a set; repeated entries and list order do not affect availability, seeded output or future RNG state. All vertices must be in range and the two normalized sets must be disjoint. Reject invalid lists even for count=0. Empty sides are valid with zero capacity. For directed sampling, only left-to-right edges belong to the view; for undirected sampling, either orientation selects the same view, and swapping the sides must preserve seeded draw order and subsequent RNG state. All returned undirected pairs remain canonical. Draw uniformly without replacement from the selected pairs that are neither forbidden nor already leased. These leases occupy the original global pool: take/release, overlapping bipartite views and clone must agree on them. Count greater than the view's current availability fails atomically, including future RNG state. Querying availability and successful empty takes do not advance the RNG. Repeated batches for the same normalized view are equivalent to one combined batch, including the later unrestricted sampled stream.

Reconfigure changes n and replaces the entire forbidden set while preserving the directed mode, outstanding endpoint pairs and RNG state. It may grow or shrink the graph, but rejects zero/overflowing n, invalid forbidden endpoints/loops, any newly forbidden leased edge, and shrinking past a leased endpoint. A failed reconfiguration leaves the whole sampler and future stream unchanged. Normalize exclusions as in new; when n and the normalized exclusions do not change, reconfigure is an exact no-op. For an actual successful change, seeded behavior is deterministic for the same prior snapshot and equivalent normalized requests; no fixed cross-implementation remapping order is required. Leases are pairs, so their meaning survives changed rank formulas and they can be released after a resize. Removed exclusions become available. Newly added edges and newly excluded edges affect both the unrestricted pool and restricted views.

The Cartesian product is implicit: a view with 50,000 vertices on each side must support sparse draws on a 100,000-node graph without enumerating its billions of edges. It is acceptable to preprocess current constraints once per restricted batch or actual reconfiguration; do not rescan them for each requested edge. Keep memory proportional to the two vertex lists, current forbidden pairs and current leases, and discard temporary view state when the batch ends. Dense tiny views must drain exactly and promptly even when almost all selected pairs are blocked by prior unrestricted draws. Validate construction/reconfiguration overflow before allocating graph-size storage. Preserve generic one-shot graph weight callbacks and all preceding sampler behavior.

## Complete representable implicit edge space

The sampler's integer-domain contract applies to every positive n whose full non-loop edge count fits usize: n*(n-1) for directed sampling and n*(n-1)/2 for undirected sampling, computed mathematically. Do not reject a representable undirected capacity merely because the unhalved product or an intermediate rank calculation overflows. Sparse sampler operations must work at this boundary without allocating n vertex records or the quadratic pool. This requirement concerns the implicit sampler; constructing a one-shot graph with billions of actual nodes is not required.

Construction, exclusions, endpoint-to-rank conversion, inverse conversion, take/release, restricted views and reconfiguration all preserve exact endpoint pairs near the maximum valid n and at its largest vertex indices. No floating-point rounding or intermediate overflow may turn a valid edge into an invalid one, wrap its identity, panic, or change its availability. A mathematically overflowing capacity must still return InvalidInputError, and failed reconfiguration must preserve leases and the RNG stream. These rules apply with duplicates, undirected reversals and small high-index views, even when the implicit edge space occupies nearly the entire usize range. Existing smaller sparse/dense, batching, uniformity and generic weight-callback requirements remain in force.

## Economical independent branching snapshots

The existing Clone implementation must support branching incremental simulations. A clone captures the complete sampler state, including RNG, current leases, exclusions and availability; changes on one branch never affect its parent, siblings or descendants captured earlier. Preserve this independence through successful and failed take/release, clone-of-clone, dropping intermediate snapshots, and the existing view/reconfiguration behavior.

Cloning a sampler with many leases or exclusions, then performing a few unrestricted take/release operations in each retained branch, must not copy the full state per branch. Structural sharing is allowed while mutable state remains independent. With S retained index records, B live branches and U local edge updates across them, shared index storage should scale with S + B + U log(S+U+1), plus the ordinary input/output vectors, rather than B*S. Clone itself must have constant work and extra storage with respect to S. Local take/release updates must not defer a full-state copy until the first mutation. Preserve the original uniform draws, batching/RNG rules, validation atomicity and exact integer-domain behavior; no fixed seeded stream across different implementations is required.

Private resource checks compare 64 retained branches from states of 1,024 and 32,768 records, separately emphasizing current leases and immutable exclusions. Each branch releases one existing lease and takes one new edge. The branches remain alive through measurement. Counting successful native global-allocator requests, including reallocation target capacities, the clone/update phase in either state size must allocate at most 32 MiB; its allocation at the larger size must be at most eight times the smaller size plus 4 MiB. Setup, initial sampling, fixture storage and final checking are outside that phase. These deliberately broad envelopes supplement the scalable-storage requirement and allow different valid representations; no internal node type, exact allocation count or elapsed-time threshold is required.

Actual reconfiguration may rebuild affected indexes, and restricted draws retain their earlier permitted once-per-batch preprocessing cost. This extension adds no public method or dependency and does not require changing the one-shot graph APIs. Document the snapshot behavior in the existing public sampler API.

## Retained local-update histories

The economical snapshot requirement also applies to long-lived incremental
histories. Repeatedly clone a modified lineage and retain its preceding
snapshots while continuing single-edge release/take updates. Every retained
snapshot preserves its own leases, availability and RNG stream; a later
update, failed operation or compaction must not change an earlier state.
Periodically copying the whole lease set or copying the entire accumulated
update log for each new retained snapshot does not satisfy the scalable
shared-index requirement above. The storage bound includes all retained
snapshots and all local updates; it does not require sharing output vectors.

A native resource fixture initializes a directed 100,000-vertex implicit
sampler with either 1,024 or 32,768 leases, then creates 16 lineages. Each
lineage performs 1,024 single-edge release/take pairs and retains a clone
after every pair; all 16,384 snapshots stay alive through measurement. The
first release uses an existing lease, and each subsequent pair releases
that lineage's preceding returned edge. Initial construction, fixture/input
storage and final semantic validation are outside allocation accounting.
Using the same successful allocator-request/reallocation accounting as the
earlier fixture, each phase may allocate at most 256 MiB, and the larger
state may allocate at most eight times the smaller state plus 16 MiB.
These broad limits permit alternative shared representations and contain no
wall-clock threshold. Keep the earlier one-update snapshot resource checks
and all graph/sampler/DAG semantics passing. No new public method or
dependency is required.

## Exact conditional DAG completions

Extend the same sampler with these documented public methods:

- `count_acyclic_completions(&self, total_edges: usize) -> Result<u128, InvalidInputError>`
- `take_acyclic_completion_by_rank(&mut self, total_edges: usize, ordinal: u128) -> Result<Vec<(usize,usize)>, InvalidInputError>`
- `take_acyclic_completion(&mut self, total_edges: usize) -> Result<Vec<(usize,usize)>, InvalidInputError>`

These methods support directed samplers with 1 through 9 vertices. On an undirected sampler or a sampler with more than 9 vertices they return InvalidInputError and preserve all state. Such samplers retain all preceding operations and their larger integer domain.

Each completion is a distinct labeled directed acyclic graph edge set on the current vertices. It contains every currently leased edge, excludes every current forbidden edge, and has exactly total_edges edges, including the existing leases. Count these graph edge sets exactly in u128. Cyclic existing leases, a total smaller than the lease count, or any other infeasible total have zero completions; a valid-domain count returns Ok(0), while either take method returns InvalidInputError. A count never mutates state or advances RNG.

For rank mode, remove the existing leases from every completed edge set, sort each remaining edge vector by (source,target), and order those vectors lexicographically. Ordinal selects that zero-based order. An ordinal outside [0,count) fails atomically. Return only the sorted newly added edges, and lease them in the same underlying pool as take/take_between. Rank mode never advances RNG. Release, availability, restricted views, reconfiguration and independent snapshots must all observe the resulting leases. Releasing the returned vector restores the prior lease pool; since rank mode did not advance RNG, the future unrestricted stream must then match the prior snapshot.

Random mode must select uniformly among the distinct final edge sets described above and return its sorted new edges. Sampling each next acyclic edge uniformly or selecting a uniformly random compatible topological order can bias this distribution. Equivalent normalized exclusions and identical seeded snapshots must give identical results and future streams within an implementation; no reference-specific PRNG sequence is required. Failed operations and successful calls requiring zero new edges preserve all indexes and the future RNG stream. A successful random completion that adds edges may advance RNG; its later state must be deterministic from the prior snapshot and request.

Exact counting and ranking must remain practical for this finite domain in ordinary Rust debug builds. The native computation fixture uses n=9, evaluates the count spectrum for final sizes 0 through 36, checks middle and endpoint ranks at 18 edges, and repeats representative ranks with nonempty required/forbidden sets. Its already-compiled worker must finish within a deliberately broad 120-second envelope. Compilation, dependency preparation, baseline checkout and the model/API run are outside that native computation phase. Smaller independently enumerated graphs verify the exact rank/count semantics; broad seeded frequency checks verify conditional uniformity without demanding an exact sequence. No internal algorithm, recurrence, type name or new dependency is prescribed. Keep all preceding generator, sparse integer-domain, snapshot and pool requirements passing.
