# Output-Level Counterfactual Consistency Summary

This report evaluates whether a causal language model assigns higher forced-choice likelihood to `yes` for identical sentence controls and to `no` for counterfactual role-reversal or negation pairs. The experiment is a dataset-only behavioral diagnostic, not a human-alignment experiment.

## Accuracy and Bias

| Model | Phenomenon | Condition | n | Accuracy | Yes-rate | Mean yes-minus-no margin |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| google/gemma-3-4b-it | negation | counterfactual | 1500 | 0.8140 | 0.1860 | -6.2187 |
| google/gemma-3-4b-it | negation | identity_control | 1500 | 1.0000 | 1.0000 | 24.7007 |
| google/gemma-3-4b-it | role_reversal | counterfactual | 1500 | 0.9687 | 0.0313 | -10.0992 |
| google/gemma-3-4b-it | role_reversal | identity_control | 1500 | 0.9993 | 0.9993 | 24.3771 |
| gpt2 | negation | counterfactual | 1500 | 0.9380 | 0.0620 | -0.4468 |
| gpt2 | negation | identity_control | 1500 | 0.2187 | 0.2187 | -0.2346 |
| gpt2 | role_reversal | counterfactual | 1500 | 0.9760 | 0.0240 | -0.5579 |
| gpt2 | role_reversal | identity_control | 1500 | 0.0393 | 0.0393 | -0.4427 |
| mistralai/Mistral-7B-Instruct-v0.3 | negation | counterfactual | 1500 | 0.6520 | 0.3480 | -2.7357 |
| mistralai/Mistral-7B-Instruct-v0.3 | negation | identity_control | 1500 | 1.0000 | 1.0000 | 20.6563 |
| mistralai/Mistral-7B-Instruct-v0.3 | role_reversal | counterfactual | 1500 | 0.7340 | 0.2660 | -4.7608 |
| mistralai/Mistral-7B-Instruct-v0.3 | role_reversal | identity_control | 1500 | 1.0000 | 1.0000 | 19.3145 |

## CSS Shift Versus Output Discrimination

For counterfactual rows, `no_margin = score(no) - score(yes)`. Positive correlations mean larger representation shifts are associated with stronger output-level rejection of the counterfactual as meaning-preserving.

| Output model | Metric model | Phenomenon | Metric | n | Spearman r | p |
| --- | --- | --- | --- | ---: | ---: | ---: |
| google/gemma-3-4b-it | bert-base-uncased | negation | delta_cos | 1500 | 0.1719 | 2.05e-11 |
| google/gemma-3-4b-it | bert-base-uncased | negation | delta_frob | 1500 | 0.1626 | 2.4e-10 |
| google/gemma-3-4b-it | bert-base-uncased | negation | delta_l2 | 1500 | 0.2462 | 3.73e-22 |
| google/gemma-3-4b-it | bert-base-uncased | negation | delta_token_aligned | 1500 | 0.2329 | 6.42e-20 |
| google/gemma-3-4b-it | bert-base-uncased | role_reversal | delta_cos | 1500 | 0.2207 | 5.35e-18 |
| google/gemma-3-4b-it | bert-base-uncased | role_reversal | delta_frob | 1500 | 0.2100 | 2.09e-16 |
| google/gemma-3-4b-it | bert-base-uncased | role_reversal | delta_l2 | 1500 | 0.2130 | 7.55e-17 |
| google/gemma-3-4b-it | bert-base-uncased | role_reversal | delta_token_aligned | 1500 | 0.1478 | 8.85e-09 |
| google/gemma-3-4b-it | gpt2 | negation | delta_cos | 1500 | 0.0625 | 0.0155 |
| google/gemma-3-4b-it | gpt2 | negation | delta_frob | 1500 | 0.1823 | 1.12e-12 |
| google/gemma-3-4b-it | gpt2 | negation | delta_l2 | 1500 | 0.0921 | 0.000354 |
| google/gemma-3-4b-it | gpt2 | negation | delta_token_aligned | 1500 | 0.0371 | 0.151 |
| google/gemma-3-4b-it | gpt2 | role_reversal | delta_cos | 1500 | 0.1305 | 3.94e-07 |
| google/gemma-3-4b-it | gpt2 | role_reversal | delta_frob | 1500 | 0.0819 | 0.0015 |
| google/gemma-3-4b-it | gpt2 | role_reversal | delta_l2 | 1500 | 0.0542 | 0.0358 |
| google/gemma-3-4b-it | gpt2 | role_reversal | delta_token_aligned | 1500 | -0.0086 | 0.74 |
| google/gemma-3-4b-it | roberta-base | negation | delta_cos | 1500 | 0.2570 | 4.68e-24 |
| google/gemma-3-4b-it | roberta-base | negation | delta_frob | 1500 | 0.2526 | 2.83e-23 |
| google/gemma-3-4b-it | roberta-base | negation | delta_l2 | 1500 | 0.3182 | 1.23e-36 |
| google/gemma-3-4b-it | roberta-base | negation | delta_token_aligned | 1500 | 0.3314 | 8.92e-40 |
| google/gemma-3-4b-it | roberta-base | role_reversal | delta_cos | 1500 | 0.1700 | 3.43e-11 |
| google/gemma-3-4b-it | roberta-base | role_reversal | delta_frob | 1500 | 0.1682 | 5.49e-11 |
| google/gemma-3-4b-it | roberta-base | role_reversal | delta_l2 | 1500 | 0.1689 | 4.62e-11 |
| google/gemma-3-4b-it | roberta-base | role_reversal | delta_token_aligned | 1500 | 0.1193 | 3.61e-06 |
| gpt2 | bert-base-uncased | negation | delta_cos | 1500 | -0.0359 | 0.165 |
| gpt2 | bert-base-uncased | negation | delta_frob | 1500 | -0.0042 | 0.872 |
| gpt2 | bert-base-uncased | negation | delta_l2 | 1500 | -0.0253 | 0.328 |
| gpt2 | bert-base-uncased | negation | delta_token_aligned | 1500 | -0.1277 | 7.02e-07 |
| gpt2 | bert-base-uncased | role_reversal | delta_cos | 1500 | 0.0444 | 0.0854 |
| gpt2 | bert-base-uncased | role_reversal | delta_frob | 1500 | 0.0233 | 0.366 |
| gpt2 | bert-base-uncased | role_reversal | delta_l2 | 1500 | 0.0554 | 0.032 |
| gpt2 | bert-base-uncased | role_reversal | delta_token_aligned | 1500 | 0.0786 | 0.00232 |
| gpt2 | gpt2 | negation | delta_cos | 1500 | 0.1592 | 5.68e-10 |
| gpt2 | gpt2 | negation | delta_frob | 1500 | 0.1257 | 1.04e-06 |
| gpt2 | gpt2 | negation | delta_l2 | 1500 | 0.0932 | 0.0003 |
| gpt2 | gpt2 | negation | delta_token_aligned | 1500 | -0.1671 | 7.36e-11 |
| gpt2 | gpt2 | role_reversal | delta_cos | 1500 | 0.0322 | 0.213 |
| gpt2 | gpt2 | role_reversal | delta_frob | 1500 | -0.0081 | 0.754 |
| gpt2 | gpt2 | role_reversal | delta_l2 | 1500 | 0.0183 | 0.479 |
| gpt2 | gpt2 | role_reversal | delta_token_aligned | 1500 | -0.0209 | 0.418 |
| gpt2 | roberta-base | negation | delta_cos | 1500 | 0.1266 | 8.77e-07 |
| gpt2 | roberta-base | negation | delta_frob | 1500 | 0.1359 | 1.26e-07 |
| gpt2 | roberta-base | negation | delta_l2 | 1500 | 0.0678 | 0.00865 |
| gpt2 | roberta-base | negation | delta_token_aligned | 1500 | -0.0676 | 0.00878 |
| gpt2 | roberta-base | role_reversal | delta_cos | 1500 | -0.0060 | 0.815 |
| gpt2 | roberta-base | role_reversal | delta_frob | 1500 | -0.0168 | 0.516 |
| gpt2 | roberta-base | role_reversal | delta_l2 | 1500 | -0.0002 | 0.992 |
| gpt2 | roberta-base | role_reversal | delta_token_aligned | 1500 | 0.0754 | 0.00348 |
| mistralai/Mistral-7B-Instruct-v0.3 | bert-base-uncased | negation | delta_cos | 1500 | 0.1735 | 1.33e-11 |
| mistralai/Mistral-7B-Instruct-v0.3 | bert-base-uncased | negation | delta_frob | 1500 | 0.1710 | 2.65e-11 |
| mistralai/Mistral-7B-Instruct-v0.3 | bert-base-uncased | negation | delta_l2 | 1500 | 0.2300 | 1.87e-19 |
| mistralai/Mistral-7B-Instruct-v0.3 | bert-base-uncased | negation | delta_token_aligned | 1500 | 0.1922 | 6.1e-14 |
| mistralai/Mistral-7B-Instruct-v0.3 | bert-base-uncased | role_reversal | delta_cos | 1500 | 0.2895 | 2.35e-30 |
| mistralai/Mistral-7B-Instruct-v0.3 | bert-base-uncased | role_reversal | delta_frob | 1500 | 0.2692 | 2.56e-26 |
| mistralai/Mistral-7B-Instruct-v0.3 | bert-base-uncased | role_reversal | delta_l2 | 1500 | 0.3030 | 3.23e-33 |
| mistralai/Mistral-7B-Instruct-v0.3 | bert-base-uncased | role_reversal | delta_token_aligned | 1500 | 0.2350 | 2.84e-20 |
| mistralai/Mistral-7B-Instruct-v0.3 | gpt2 | negation | delta_cos | 1500 | 0.0983 | 0.000137 |
| mistralai/Mistral-7B-Instruct-v0.3 | gpt2 | negation | delta_frob | 1500 | 0.1969 | 1.41e-14 |
| mistralai/Mistral-7B-Instruct-v0.3 | gpt2 | negation | delta_l2 | 1500 | 0.0258 | 0.319 |
| mistralai/Mistral-7B-Instruct-v0.3 | gpt2 | negation | delta_token_aligned | 1500 | 0.0098 | 0.703 |
| mistralai/Mistral-7B-Instruct-v0.3 | gpt2 | role_reversal | delta_cos | 1500 | 0.1048 | 4.77e-05 |
| mistralai/Mistral-7B-Instruct-v0.3 | gpt2 | role_reversal | delta_frob | 1500 | 0.0713 | 0.00574 |
| mistralai/Mistral-7B-Instruct-v0.3 | gpt2 | role_reversal | delta_l2 | 1500 | 0.0542 | 0.0357 |
| mistralai/Mistral-7B-Instruct-v0.3 | gpt2 | role_reversal | delta_token_aligned | 1500 | -0.0205 | 0.427 |
| mistralai/Mistral-7B-Instruct-v0.3 | roberta-base | negation | delta_cos | 1500 | 0.2487 | 1.38e-22 |
| mistralai/Mistral-7B-Instruct-v0.3 | roberta-base | negation | delta_frob | 1500 | 0.2515 | 4.54e-23 |
| mistralai/Mistral-7B-Instruct-v0.3 | roberta-base | negation | delta_l2 | 1500 | 0.3005 | 1.1e-32 |
| mistralai/Mistral-7B-Instruct-v0.3 | roberta-base | negation | delta_token_aligned | 1500 | 0.2760 | 1.25e-27 |
| mistralai/Mistral-7B-Instruct-v0.3 | roberta-base | role_reversal | delta_cos | 1500 | 0.2390 | 6.29e-21 |
| mistralai/Mistral-7B-Instruct-v0.3 | roberta-base | role_reversal | delta_frob | 1500 | 0.2260 | 7.84e-19 |
| mistralai/Mistral-7B-Instruct-v0.3 | roberta-base | role_reversal | delta_l2 | 1500 | 0.2449 | 6.25e-22 |
| mistralai/Mistral-7B-Instruct-v0.3 | roberta-base | role_reversal | delta_token_aligned | 1500 | 0.1900 | 1.18e-13 |
