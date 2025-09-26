import pandas as pd

# # --- T-TEST PHRASES ---
# ttest_file = '..\\data\\stats\\ttest_saccades.csv'  # À adapter selon le fichier voulu
# try:
#     df_t = pd.read_csv(ttest_file)
#     # Columns : Measure, T_statistic, P_value, Mean_first_minute, Mean_last_minute
#     for idx, row in df_t.iterrows():
#         measure = row['Measure']
#         direction = "an increase" if row['Mean_last_minute'] > row['Mean_first_minute'] else "a decrease"
#         mean_first = row['Mean_first_minute']
#         mean_last = row['Mean_last_minute']
#         stat_value = row['T_statistic']
#         p_value = row['P_value']
#         if p_value < 0.05:
#             phrase = (
#                 f"Participants showed {direction} in the {measure.replace('_', ' ').lower()} during the last minute "
#                 f"(mean = {mean_last:.2f}) compared to the first minute (mean = {mean_first:.2f}) "
#                 f"(t = {stat_value:.2g}, p = {p_value:.3g})."
#             )
#             print(phrase)
#         else:
#             phrase = (
#                 f"There was no significant difference in the {measure.replace('_', ' ').lower()} between the first minute "
#                 f"(mean = {mean_first:.2f}) and the last minute (mean = {mean_last:.2f}) "
#                 f"(t = {stat_value:.2g}, p = {p_value:.3g})."
#             )
#             print(phrase)
# except FileNotFoundError:
#     pass

# --- WILCOXON GROUP COMPARISON PHRASES ---
wilcoxon_file = '..\\data\\stats\\wilcoxon_saccades-diff_second.csv'
try:
    df_w = pd.read_csv(wilcoxon_file)
    # Columns: Measure, Wilcoxon_statistic, P_value, Mean_simplified, Mean_enriched
    for idx, row in df_w.iterrows():
        measure = row['Measure']
        mean_simplified = row['Mean_simplified']
        mean_enriched = row['Mean_enriched']
        stat_value = row['Wilcoxon_statistic']
        p_value = float(row['P_value'])
        if p_value < 0.05:
            if mean_enriched > mean_simplified:
                direction = "higher"
            elif mean_enriched < mean_simplified:
                direction = "lower"
            else:
                direction = "equal"
            phrase = (
                f"The enriched group showed a {direction} {measure.replace('_', ' ').lower()} (mean = {mean_enriched:.2f}) "
                f"compared to the simplified group (mean = {mean_simplified:.2f}) "
                f"(Wilcoxon U = {stat_value:.2g}, p = {p_value:.3g})."
            )
            print(phrase)
        else:
            phrase = (
                f"There was no significant difference in the {measure.replace('_', ' ').lower()} between the enriched group "
                f"(mean = {mean_enriched:.2f}) and the simplified group (mean = {mean_simplified:.2f}) "
                f"(Wilcoxon U = {stat_value:.2g}, p = {p_value:.3g})."
            )
            print(phrase)
except FileNotFoundError:
    pass
        
# input_file_s = '..\\data\\stats\\ttest_grouped_saccades.csv'
# df_s = pd.read_csv(input_file_s)
# # Columns : T_stat,T_pvalue,First_mean,First_sd,Last_mean,Last_sd

# for idx, row in df_s.iterrows():
#     direction = "increased" if row['Last_mean'] > row['First_mean'] else "decreased"
#     if row['T_pvalue'] < 0.05:
#         print(
#             f"The mean number of saccades {direction} from the first minute "
#             f"(mean={row['First_mean']:.2f}, sd={row['First_sd']:.2f}) to the last minute "
#             f"(mean={row['Last_mean']:.2f}, sd={row['Last_sd']:.2f}) "
#             f"(t={row['T_stat']:.2f}, p={row['T_pvalue']:.3g})."
#         )
#     else:
#         print(
#             f"There was no significant difference in the mean number of saccades between the first minute "
#             f"(mean={row['First_mean']:.2f}, sd={row['First_sd']:.2f}) and the last minute "
#             f"(mean={row['Last_mean']:.2f}, sd={row['Last_sd']:.2f}) "
#             f"(t={row['T_stat']:.2f}, p={row['T_pvalue']:.3g})."
#         )
        
# input_file_w = '..\\data\\stats\\wilcoxon_grouped.csv'
# df_w = pd.read_csv(input_file_w)
# # Columns : T_stat,T_pvalue,First_mean,First_sd,Last_mean,Last_sd

# for idx, row in df_w.iterrows():
#     if row['MannWhitney_p'] < 0.05:
#         print(
#             f"The mean value for {row['Group']} {row['Direction'].lower()} from the first minute "
#             f"(mean={row['Mean_first']:.2f}, sd={row['SD_first']:.2f}) to the last minute "
#             f"(mean={row['Mean_last']:.2f}, sd={row['SD_last']:.2f}) "
#             f"(Wilcoxon/Mann-Whitney U={row['MannWhitney_stat']:.2f}, p={row['MannWhitney_p']:.3g})."
#         )
#     else:
#         print(
#             f"There was no significant difference in the mean value for {row['Group']} between the first minute "
#             f"(mean={row['Mean_first']:.2f}, sd={row['SD_first']:.2f}) and the last minute "
#             f"(mean={row['Mean_last']:.2f}, sd={row['SD_last']:.2f}) "
#             f"(Wilcoxon/Mann-Whitney U={row['MannWhitney_stat']:.2f}, p={row['MannWhitney_p']:.3g})."
#         )