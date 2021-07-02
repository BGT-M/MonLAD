# MonLAD

Here we provide MonLAD code.

### About code

- **Data**: Due to the privacy of bank data, we only provide a demo data to help users better use it.
- **Input format**: We provide two input formats corresponding to different files (i.e., ZeroOutCore.py and ZeroOutCoreCFD.py).
  - (source_id, destination_id, timestamp, weight)   corr. to `ZeroOutCore.py`
  - (account_id, transaction_type, weight) corr. to `ZeroOutCoreCFD.py`
    - Note that: If you choose the second one, you may need to change the name of the transaction_type in `ZeroOutCoreCFD.py`,  that is, `PRIJEM` represents transfer in  and `VYDAJ` represents transfer out.
- **Parameters** (default) :
  - MonLAD: `delta_up = delta_down = epsilon = 10k`
  - AnoScore: `alpha = 0.5, p = 0.8, k = 1`
    - For normal data,  it is recommended to set `alpha = 0.98, k = 1.5, p = 0.9~0.99`.
