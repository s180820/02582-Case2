import pandas as pd
import os
from tqdm import tqdm

def build_dataframe(signal="BVP"):
    """
    Build a dataframe from the dataset folder
    :param signal: the signal to extract
    :return: a dataframe containing the signal

    Possible signals:
    - BVP: Blood Volume Pulse
    - EDA: Electrodermal Activity
    - TEMP: Temperature
    - HR: Heart Rate
    - response: response to the questionnaire
    """
    df = pd.DataFrame()
    for dirname, _, filenames in os.walk('dataset'):
        for filename in filenames:
            try:
                _, group, ID, round, phase = dirname.split("/")
            except ValueError:
                _, group, ID, ID2, round, phase = dirname.split("/")
            # create dataframe from csv file
            if filename.startswith(signal):
                tmp_df = pd.read_csv(os.path.join(dirname, filename))
                tmp_df["group"] = group
                if group == "D1_3":
                    tmp_df["sub_group"] = ID
                    tmp_df["ID"] = int(ID2[-1])
                else:
                    tmp_df["ID"] = int(ID[-1])
                tmp_df["round"] = int(round[-1])
                tmp_df["phase"] = int(phase[-1])
                tmp_df["time_point"] = range(len(tmp_df))
                df = pd.concat([df, tmp_df], axis=0)
        
    if signal == "response":
        df.sort_values(by=['group', 'sub_group', 'ID', 'round', 'phase'], inplace=True)
    else:
        df.sort_values(by=['group', 'sub_group', 'ID', 'round', 'phase', 'time'], inplace=True)
    df.drop(columns=['Unnamed: 0'], inplace=True)
    return df