import datetime
import glob
import os

import pandas as pd
import numpy as np

from tqdm import tqdm


def preprocess_train_first(before_dir, after_dir, start=0, end=31):
    print(list(filter(os.path.isdir, sorted(glob.glob(os.path.join(before_dir, "user*")))))[start:end])
    for user_folder in list(filter(os.path.isdir, sorted(glob.glob(os.path.join(before_dir, "user*")))))[start:end]:
        user_df = None
        user_id = os.path.basename(user_folder)
        
        for session_folder in tqdm(sorted(glob.glob(os.path.join(user_folder, "*")))):
            session_id = os.path.basename(session_folder)
            session_date = datetime.datetime.fromtimestamp(int(session_id), datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y%m%d')
            file_name = f"{user_id}_{session_date}.pkl"
            if os.path.join(after_dir, file_name) in glob.glob(os.path.join(after_dir, "*")):
                print(f"Skipping {file_name} because it already exists")
                continue
            session_df = None
            for sensor_folder in filter(os.path.isdir, sorted(glob.glob(os.path.join(session_folder, "*")))):
                sensor_type = os.path.basename(sensor_folder)

                train_df = None
                for timestamp_csv in sorted(glob.glob(os.path.join(sensor_folder, "*.csv"))):
                    tmp = pd.read_csv(timestamp_csv)
                    # timestamp 열에 파일 이름 숫자를 더하기
                    tmp["timestamp"] += float(os.path.basename(timestamp_csv).split(".")[0])
                    tmp["time"] = pd.to_datetime(tmp['timestamp'], unit='s', utc=True).dt.tz_convert('Asia/Seoul')
                    tmp.set_index("time", inplace=True)

                    
                    train_df = tmp if train_df is None else pd.concat([train_df, tmp])

                if train_df is None:
                    continue
                train_df.columns = [sensor_type + "_" + train_df.columns]
                session_df = train_df if session_df is None else pd.concat([session_df, train_df], join="outer", axis=1)
            
            train_action_df = pd.read_csv(os.path.join(session_folder, f"{session_id}_label.csv"))
            train_action_df["time"] = pd.to_datetime(train_action_df['ts'], unit='s', utc=True).dt.tz_convert('Asia/Seoul')
            train_action_df.set_index("time", inplace=True)
            train_action_df = train_action_df[["activity"]]
            train_action_df.rename(columns={"activity": "m_activity"}, inplace=True)
            train_action_df = train_action_df[~train_action_df.index.duplicated(keep='first')]
            train_action_df = train_action_df.resample('1s').ffill()
            train_action_df = pd.get_dummies(train_action_df, columns=['m_activity'])
            for col in train_action_df.columns:
                train_action_df[col] = train_action_df[col].astype(np.int8)


            def rename_col(col):
                if isinstance(col, tuple):
                    tmp = '_'.join(col).strip()
                    if tmp.startswith('m'):
                        tmp = "m_" + tmp[1:].lower()
                    else: # e4
                        tmp = "s_" + tmp[2:].lower()
                return tmp
            
            session_df.columns = [rename_col(col) for col in session_df.columns]
            timestamp_columns = [col for col in session_df.columns if col.endswith('_timestamp')]
            session_df.drop(columns=timestamp_columns, inplace=True)
            
            session_df = session_df.resample('1s').mean().interpolate(method='time')
            session_df = session_df.merge(train_action_df, on='time', how='outer')

            session_df.fillna(method='ffill', inplace=True)
            session_df.fillna(method='bfill', inplace=True)

            for i in range(9):
                if f'm_activity_{i}' not in session_df.columns:
                    session_df[f'm_activity_{i}'] = np.int8(0)
                elif f'm_activity_{i}' in session_df.columns:
                    session_df[f'm_activity_{i}'] = session_df[f'm_activity_{i}'].astype(np.int8)

            # save file
            os.makedirs(after_dir, exist_ok=True)
            user_df = session_df if user_df is None else pd.concat([user_df, session_df])
        os.makedirs(after_dir, exist_ok=True)
        # print(user_df.info())
        user_df.to_pickle(os.path.join(after_dir, f"{user_id}.pkl"))
        print(f"{user_id} preprocess done")
    return


def preprocess_train_second_add_activity(preprocessed_dir_ts, output_dir):
    for user in tqdm(range(1, 31)):
        try:
            user_df = pd.read_pickle(os.path.join(preprocessed_dir_ts, "train", f"user{user:02d}.pkl"))
        except Exception as e:
            print(e)
            continue
        
        rename_dict_train = {
        's_hr_hr': 's_heart_rate',
        'm_gps_lat': 'm_gps_latitude',
        'm_gps_lon': 'm_gps_longitude'}

        # m_activity 컬럼이 없는지 확인하고 없으면 추가
        for i in range(9):
            if f'm_activity_{i}' not in user_df.columns:
                user_df[f'm_activity_{i}'] = None
        user_df.drop(columns=['s_acc_x', 's_acc_y', 's_acc_z', 's_bvp_value', 's_eda_eda', 's_temp_temp',
                        'm_gps_accuracy', 'm_gyr_x', 'm_gyr_y', 'm_gyr_z', 'm_gyr_roll', 'm_gyr_pitch',
                        'm_gyr_yaw', 'm_mag_x', 'm_mag_y', 'm_mag_z'], inplace=True, errors='ignore')
        user_df.rename(columns=rename_dict_train, inplace=True)
        user_df = user_df[['m_acc_x', 'm_acc_y', 'm_acc_z',
                        'm_gps_latitude', 'm_gps_longitude', 's_heart_rate',
                        'm_activity_0', 'm_activity_1', 'm_activity_2', 'm_activity_3',
                        'm_activity_4', 'm_activity_5', 'm_activity_6', 'm_activity_7', 'm_activity_8']]

        resample_dict_10_min = {
            'm_acc_x': ['mean', 'std', 'min', 'max'],
            'm_acc_y': ['mean', 'std', 'min', 'max'],
            'm_acc_z': ['mean', 'std', 'min', 'max'],
            'm_gps_latitude': ['mean', 'std', 'min', 'max'],
            'm_gps_longitude': ['mean', 'std', 'min', 'max'],
            's_heart_rate': ['mean', 'std', 'min', 'max'],
            'm_activity_0': ['max'],
            'm_activity_1': ['max'],
            'm_activity_2': ['max'],
            'm_activity_3': ['max'],
            'm_activity_4': ['max'],
            'm_activity_5': ['max'],
            'm_activity_6': ['max'],
            'm_activity_7': ['max'],
            'm_activity_8': ['max']
        }
        # resample
        user_df = user_df.resample('10min').agg(resample_dict_10_min)

        # # 컬럼명 수정
        user_df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in user_df.columns]
        user_df.ffill(inplace=True)
        user_df.bfill(inplace=True)

        os.makedirs(output_dir, exist_ok=True)
        user_df.to_pickle(os.path.join(output_dir, f"user{user:02d}.pkl"))