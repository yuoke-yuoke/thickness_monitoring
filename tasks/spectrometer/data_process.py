import os
import csv
import numpy



class DataProcess():

    def __init__(self):
        
        self.folder_path = "E:\\reserch\\241025\\spec\\3-1_5-1_slimonene"
        self.output_file = "E:\\reserch\\241025\\spec\\3-1_5-1.csv"
        self.name_time_file = "E:\\reserch\\241016_humidity\\spec\\6-1_name_time.csv"
        self.mirror_path = "E:\\reserch\\241025\\spec\\mirror000000000.txt"
        self.current_file = ""

        self.min = 500
        self.max = 750

        self.extension = ".txt"
        self.delimiter = ";"

        self.reflective_points = []
        self.reflective_values = []

        self.start_row = None
        self.end_row = None

        self.csv_files = []
        self.time_files = []
        self.time_files_shortened = []
        self.time_files_absolute = []
        self.output_list = []
        self.mirror_int = []
        self.firstrow = []
        self.wavelength: numpy.ndarray # 

        self.initial_time = 0
        self.time = self.initial_time
        self.step = 0

    def get_relative_time(self):

        time_files = []

        self.current_file = os.path.join(self.folder_path, self.csv_files[0])
        time0s = os.path.getctime(os.path.join(self.folder_path, self.current_file))
        
        for csv_file in self.csv_files:
            path = os.path.join(self.folder_path, csv_file)
            creation_time = os.path.getctime(path)
            self.time_files_absolute.append(creation_time)
            time_files.append(creation_time - time0s)

        return time_files


    def row_range(self, file_path: str):

        firstrow = []

        # CSVファイルをセミコロン区切りで読み込む
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            
            for row_num, row in enumerate(reader):
                try:
                    # 1列目の値をfloatに変換
                    value = float(row[0])

                    if value >= self.max:
                        self.end_row = row_num
                        break
                    if value >= self.min:
                        firstrow.append(value)
                        if self.start_row is None:
                            self.start_row = row_num

                except ValueError:
                    # 1列目が数値でない場合は無視
                    continue

        # 結果の出力
        if self.start_row is not None and self.end_row is None:
            self.end_row = row_num  # 750未満の最後まで該当していた場合

        self.firstrow = firstrow

    def wl_range_array(self, wavelengths: numpy.ndarray):
        for wl_num, wl in enumerate(wavelengths):
            try: 
                value = float(wl)
                if self.start_row:
                    if value >= self.max:
                        self.end_row = wl_num
                        break
                else:
                    if value >= self.min:
                        self.start_row = wl_num
            except ValueError:
                continue
        if self.start_row is not None and self.end_row is None:
            self.end_row = wl_num

        self.wavelength = wavelengths[self.start_row:self.end_row]



    def pick_points_value(self, file_path: str):


        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            l = [_ for _ in reader]

            for point_num, point in enumerate(self.reflective_points):
                try:
                    ref = float(l[point][1])
                    self.reflective_values[point_num].append(ref)
                except ValueError:
                    continue        

    def get_extrema(self, inc: bool = True):

        self.settings()

        for i in range(len(self.reflective_points)):
            self.reflective_points[i] += self.start_row
            

        self.reflective_values = [[] for _ in range(len(self.reflective_points))]

        for file_num, csv_file in enumerate(self.csv_files):
            file_path = os.path.join(self.folder_path, csv_file)
            self.pick_points_value(file_path)
        
        result = []
        
        prev_value = 0
        prev_index = 0
        if inc == False: # 最初の傾きが負
            prev_value = 100


        for file_num, reflective_value in enumerate(self.reflective_values[0]):
            if inc: # 増加する方
                if prev_value > reflective_value:
                    result.append(prev_index)
                    inc = False
            else:
                if prev_value < reflective_value:
                    result.append(prev_index)
                    inc = True

            prev_value = reflective_value
            prev_index = file_num

        return result

    def mirror(self, file_path: str):
        rows = []

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)

            row_count = 0

            for row in reader:
                try:
                    rows.append(float(row[1]))
                    row_count+=1
                except ValueError:
                    continue
                except IndexError:
                    continue
            
        return rows


    def settings(self):

        self.csv_files = [f for f in os.listdir(self.folder_path) if f.endswith(self.extension)]

        self.time_files = self.get_relative_time()

        self.row_range(os.path.join(self.folder_path, self.csv_files[0]))

        self.output_list.append(self.firstrow)

        self.mirror_int = self.mirror(self.mirror_path)

    def smallest_min(self, file_num: int): # 1分ごとにデータを取り出したいとき
        time = int(self.time_files[file_num])
        if time != self.time:
            self.time = time
            return True
        return False

    def pick_closest(self, file_num: int): # 初期値がself.initial_time, ステップがself.step, になるもっとも小さいファイルを抜き出す
        time = self.time_files[file_num]

        if time >= self.time:
            self.time += self.step 
            return True
        return False
    

    def get_reflectives(self, file_path: str):

        rows = []
        mirror = self.mirror_int

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)

            row_count = 0

            for row in reader:
                if row_count >= self.start_row:
                    if row_count < self.end_row:
                        rows.append(float(row[1])/float(mirror[row_count]))
                    else:
                        break
                row_count += 1
            
        return rows



    def write_lists_to_csv(self):

        self.settings()

        list1 = self.csv_files
        list2 = self.time_files
        filename = self.name_time_file

        # リストの長さが一致していることを確認
        if len(list1) != len(list2):
            raise ValueError("リストの長さが一致していません。")

        # CSVファイルに書き込む
        with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['name', 'time'])  # ヘッダーを書き込む

            # 各要素をCSVファイルに書き込む
            for i in range(min(len(list1), len(list2))):
                writer.writerow([list1[i], list2[i]])




    def write_output(self): # csv を吐き出す
        self.time_files = [""] + self.time_files
        data_rows = [self.time_files] + list(zip(*self.output_list))

        with open(self.output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data_rows)

    def main_step(self): # 1分毎に取り出すやつ
        self.settings()

        for file_num, csv_file in enumerate(self.csv_files):
            self.current_file = csv_file
            
            # if file_num % 6 == 0:
            # if self.smallest_min(file_num): # 1分ごとにデータを取り出したいときのみ
            if self.pick_closest(file_num):
                self.time_files_shortened.append(self.time_files[file_num])
                file_path = os.path.join(self.folder_path, csv_file)
                rows = self.get_reflectives(file_path)
                self.output_list.append(rows)
        self.time_files = self.time_files_shortened

        self.write_output()

    def main_extrema(self, inc_main):
        self.settings()

        list_extrema = self.get_extrema(inc=inc_main)

        for i in range(len(list_extrema)):
            if i%2 == 1:
                file_num = list_extrema[i]
                csv_file = self.csv_files[file_num]
                self.current_file = csv_file

                self.time_files_shortened.append(self.time_files[file_num])
                file_path = os.path.join(self.folder_path, csv_file)
                rows = self.get_reflectives(file_path)
                self.output_list.append(rows)

        self.time_files = self.time_files_shortened
        self.write_output()


    def main_all(self): # フォルダをすべて
        self.settings()

        for file_num, csv_file in enumerate(self.csv_files):
            self.current_file = csv_file
            
            self.time_files_shortened.append(self.time_files[file_num])
            file_path = os.path.join(self.folder_path, csv_file)
            rows = self.get_reflectives(file_path)
            self.output_list.append(rows)
        self.time_files = self.time_files_shortened # タイトルを基準からの時間にしたいとき
        # self.time_files = self.csv_files

        self.write_output()



if __name__ == "__main__":
    dp = DataProcess()

    dp.folder_path = r"E:\reserch\241025\spec\3-1_5-1_slimonene"
    dp.output_file = r"E:\reserch\241025\spec\5-1_extrema.csv"
    dp.name_time_file = r"E:\reserch\241025\spec\3-1_name_time.csv"
    dp.mirror_path = r"E:\reserch\241025\spec\mirror000000000.txt"

    dp.extension = ".txt"
    dp.initial_time = 0
    dp.step = 0.5

    # dp.reflective_points = [226, 1090] 4-1, 6-1
    dp.reflective_points = [0, 666]


    # dp.main_step()
    # dp.main_all()
    # dp.write_lists_to_csv()
    # dp.get_extrema(inc =True)
    dp.main_extrema(inc_main=False)