import tkinter as tk
import pandas as pd

class MassFlowHandler:
    def __init__(self, logic, ui):
        self.logic = logic
        self.ui = ui
        if self.ui:
            self.ui.set_handler(self)

    def import_preset(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])

        if file_path:
            try:
                df = pd.read_excel(file_path, sheet_name='出力電圧(V)', engine="openpyxl")
                df_cleaned = df.dropna(thresh=4)
                # print(type(df_cleaned))
                # print(df_cleaned)
                # print(df_cleaned.iloc[1:])
                # print(df_cleaned.iloc[1])
                self.logic.instructions.flow_list = None
                self.logic.instructions.flow_list = df_cleaned.iloc[1:].values.tolist()

            except Exception as e:
                print(f"Error importing preset: {e}")

    def show_data(self):
        formatted_rows = [
            " ".join(cell.ljust(7) for cell in row)
            for row in self.logic.instructions.flow_title + self.logic.instructions.flow_list
        ]
        return formatted_rows

    def highlight_row(self, tree, cur_index):
        tree.tag_configure("highlight", background="yellow")

        n_rows = len(tree.get_children())
        for i in range(n_rows):
            item = tree.get_children()[i]
            tree.item(item, tags=())

        # 新しい行をハイライト
        item = tree.get_children()[cur_index]
        tree.item(item, tags=("highlight",))

    def update_listbox(self, tree, cur_index=0):
        # self.data_listbox2 = ttk.Treeview(self.preset_frame, columns=self.instructions.flow_title[0], show="headings", height=8)
        for title in self.logic.instructions.flow_title[0]:
            tree.heading(title, text=title)
            tree.column(title, width=60, anchor="e")
        tree.delete(*tree.get_children())
        for row in self.logic.instructions.flow_list:
            tree.insert("", tk.END, values=list(row))
        tree.place(x=0, y=0)

        self.highlight_row(tree, cur_index=cur_index)
        print(self.logic.instructions.flow_list)
