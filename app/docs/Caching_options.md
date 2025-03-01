Is Caching Useful Here?
Limited Usefulness: In the exact form described, caching might have limited usefulness because users are unlikely to enter exactly the same query multiple times. This results in frequent cache misses, where the system has to compute the vector anyway.

Advanced Caching Strategies:

N-Gram or Partial Matching: Instead of caching whole queries, you could cache parts of queries (e.g., "near ostsee", "in stralsund"). When a new query comes in, the system could potentially reuse parts of previously cached vectors.
Semantic Caching: Another advanced approach could involve caching based on the semantic similarity of queries. For example, if "house near ostsee" and "wohnung near ostsee" produce similar vectors, the cache could be leveraged to speed up the second query by reusing or adjusting the first vector. However, this requires more sophisticated logic and might not always be accurate.
Search Result Caching: Instead of caching just the vectors, you could also cache the search results from the Elasticsearch database. If a query is similar to a recent one, the system could retrieve results faster by leveraging the cache.
Conclusion
Caching is a standard optimization technique, but its effectiveness in your scenario depends on how often users repeat the exact same queries.

For most real-world scenarios with varied search inputs like the ones you've described, simple caching based on the entire query might have limited benefits. However, more advanced caching strategies that consider partial matches, semantic similarity, or even caching search results from Elasticsearch could improve performance.

Ultimately, whether caching is useful will depend on your specific use case, the frequency of repeated queries, and how sophisticated your caching strategy is. For highly dynamic search inputs, caching might need to be combined with other performance optimizations (e.g., model optimizations, hardware acceleration) to achieve the desired speed.