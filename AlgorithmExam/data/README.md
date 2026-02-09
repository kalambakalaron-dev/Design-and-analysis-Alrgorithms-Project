# Algorithm Complexity Analysis: Prelim Exam

## Executive Summary
This project evaluates the performance of three fundamental sorting algorithms (Bubble, Insertion, and Merge Sort) using a dataset of 100,000 records. The goal is to observe the practical impact of Time Complexity (Big O).

## Benchmark Results (in Seconds)
| Algorithm | N = 1,000 | N = 10,000 | N = 100,000 |
| :--- | :--- | :--- | :--- |
| Bubble Sort | 0.1149 | 5.8048 | 1427.7027 |
| Insertion Sort | 0.1292 | 2.9901 | 710.6688 |
| Merge Sort | 0.1191 | 0.1266 | 0.4016 |

## Analysis & Conclusion
The data clearly illustrates the difference between $O(n^2)$ and $O(n \log n)$ complexities:
1. **Merge Sort** remained consistently fast, handling 100,000 records in under half a second.
2. **Bubble Sort** showed exponential growth; as the data increased 100x (from 1k to 100k), the time increased by over 12,000x.
3. **Conclusion:** For large-scale data processing, Merge Sort is the only viable option among the three tested.