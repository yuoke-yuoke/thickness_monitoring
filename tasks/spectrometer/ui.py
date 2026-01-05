import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tasks.spectrometer.spec_result import SpectrometerResultsFrame
import time
from common.eventbus import global_eventbus

class SpecUI(tk.Frame):
    def __init__(self, master, instructions, logic):
        super().__init__(master)
        self.handler = None

        self.instructions = instructions
        self.logic = logic

        self.setting_frame = tk.Frame(master, height=160, width=300, padx=10, pady=10, bg="PeachPuff1")
        self.aquire_frame = tk.Frame(master, height=160, width=200, padx=10, pady=10, bg="PeachPuff2")
        self.result_frame = tk.Frame(master, height=400, width=300, padx=0, pady=0)
        self.legend_frame = tk.Frame(master, height=400, width=200, padx=10, pady=10)

        self.setting_frame.grid(row=0, column=0)
        self.aquire_frame.grid(row=0, column=1)
        self.result_frame.grid(row=1, column=0)
        self.legend_frame.grid(row=1, column=1)

        self.SpecRF = SpectrometerResultsFrame(self.result_frame)
        self.SpecRF.grid(row=0, column=0)

        self._build_ui()

        global_eventbus.subscribe("spec_update_ui", self.update_info)
        # self.set_handler(self.logic.handler)
        # self.update_initial_ui()

    def _build_ui(self):
        # ここにUIコンポーネントを構築するコードを追加
        self.aquire_label = tk.Label(self.aquire_frame, text="Spectrum")
        self.aquire_label.place(x=0,y=0)
        self.take_spec_button = tk.Button(self.aquire_frame, text="Get", width=10, height=1)
        self.take_spec_button.place(x=0, y=30)
        self.import_spec_button = tk.Button(self.aquire_frame, text="Import", width=10, height=1)
        self.import_spec_button.place(x=0,y=60)
        self.export_spec_button = tk.Button(self.aquire_frame, text="Export", width=10, height=1)
        self.export_spec_button.place(x=0, y=90)
        self.set_as_reference_button = tk.Button(self.aquire_frame, text="Set as\nreference", width=10, height=1)
        self.set_as_reference_button.place(x=0, y=120)
        # self.take_spectra_chebox = tk.Checkbutton(self.specta_frame, text="Take spectra\n along stage motion")
        # self.take_spectra_chebox.place(x=100, y=60)
        # self.take_spectra_chebox.pack()

        self.setting_label = tk.Label(self.setting_frame, text="Settings")
        self.setting_label.place(x=0, y=0)
        self.exposure_label = tk.Label(self.setting_frame, text="Exposure (s): ")
        self.exposure_label.place(x=0, y=30)
        self.exposure_box = tk.Entry(self.setting_frame, width=23)
        # self.exposure_box.insert(tk.END, self.exposure)
        self.exposure_box.place(x=90, y=30)

        self.spec_ave_label = tk.Label(self.setting_frame, text="Average: ")
        self.spec_ave_label.place(x=0, y=60)
        self.spec_ave_box = tk.Entry(self.setting_frame, width=23)
        # self.spec_ave_box.insert(tk.END, self.logic.spec_ave)
        self.spec_ave_box.place(x=90, y=60)

        self.save_directory_label = tk.Label(self.setting_frame, text="Directory: ")
        self.save_directory_label.place(x=0, y=90)
        self.save_directory_box = tk.Entry(self.setting_frame, width=16)
        self.save_directory_box.place(x=90, y=90)
        self.directory_button = tk.Button(self.setting_frame, text="Open..", width=5, height=1) #, command=self.handler.spec_directory_button)
        self.directory_button.place(x=195, y=90)

        self.spec_name = tk.Label(self.setting_frame, text="File prefix: ")
        self.spec_name.place(x=0, y=120)
        self.spec_name_box = tk.Entry(self.setting_frame, width=23)
        self.spec_name_box.place(x=90, y=120)

        self.legend_treeview = ttk.Treeview(self.legend_frame, columns=self.instructions.legend_title, show="headings", height=15)
        self.legend_treeview.place(x=0, y=0)
        self.reference_take_label = tk.Label(self.legend_frame, text=f"Reference:\n{self.instructions.ref_time}")
        self.reference_take_label.place(x=0, y=330)


        # self.show_spectra_button = tk.Button(self.specta_frame, text="Show current\n spectra", width=10, height=3)
        # self.show_spectra_button.place(x=280, y=0)
        # self.save_spectra_button = tk.Button(self.specta_frame, text="Save spectra", width=10, height=3)
        # self.save_spectra_button.place(x=280, y=50)



    def update_initial_ui(self):
        self.take_spec_button = tk.Button(self.aquire_frame, text="Get", width=20, height=1, command=self.handler._get_button)
        self.take_spec_button.place(x=0, y=30)
        self.import_spec_button = tk.Button(self.aquire_frame, text="Import", width=20, height=1, command=self.handler.ImportData)
        self.import_spec_button.place(x=0,y=60)
        self.export_spec_button = tk.Button(self.aquire_frame, text="Export", width=20, height=1, command=self.handler.export_data_button)
        self.export_spec_button.place(x=0, y=90)
        
        self.exposure_box.insert(tk.END, self.instructions.exposuretime.value)
        self.spec_ave_box.insert(tk.END, self.instructions.spec_ave)
        self.directory_button = tk.Button(self.setting_frame, text="Open...", width=5, height=1, command=self.handler.spec_directory_button)
        self.directory_button.place(x=195, y=90)
        self.set_as_reference_button = tk.Button(self.aquire_frame, text="Set as reference", width=20, height=1, command=self.handler.set_as_reference)
        self.set_as_reference_button.place(x=0, y=120)

        self.legend_treeview.bind('<<TreeviewSelect>>', self.handler.listclick)
        self.legend_treeview.place(x=0, y=0)
        # self.show_spectra_button = tk.Button(self.aquire_frame, text="Show current\n spectra", width=10, height=3, command=self.handler.show_spectra)
        # self.show_spectra_button.place(x=280, y=0)
        # self.save_spectra_button = tk.Button(self.aquire_frame, text="Save spectra", width=10, height=3, command=self.handler.spec_directory)
        # self.save_spectra_button.place(x=280, y=50)

    def set_handler(self, handler):
        self.handler = handler
        self.update_initial_ui()
        self.update_treeview(self.legend_treeview)

    def update_info(self):
        self.handler.get_values_from_gui()
        
        # print("sel_index", self.instructions.sel_index)
        # print("cur_pos", self.instructions.cur_pos)

        self.exposure_box.delete(0, tk.END)
        self.exposure_box.insert(tk.END, self.instructions.exposuretime.value)

        self.spec_ave_box.delete(0, tk.END)
        self.spec_ave_box.insert(tk.END, self.instructions.spec_ave)

        self.save_directory_box.delete(0, tk.END)
        self.save_directory_box.insert(tk.END, self.instructions.dest_folder_path)
        self.reference_take_label.config(text=f"Reference:\n{time.strftime("%H:%M:%S", time.localtime(self.instructions.ref_time))}")
        # print("ref_time", self.instructions.ref_time)

        self.SpecRF.update_raw(self.instructions.wavelength_array, self.instructions.reference_array, self.instructions.spec_array)
        self.SpecRF.update_intfere(self.instructions.wavelength_array, self.instructions.reference_array, self.instructions.spec_array)

        self.update_treeview(self.legend_treeview)

    def update_treeview(self, tree, sel_index:int =0):
        for title in self.instructions.legend_title:
            tree.heading(title, text=title)
            tree.column(title, width=50, anchor="center")
        tree.delete(*tree.get_children())
        for i in range(self.instructions.pos_num):
            for j in range(self.instructions.loop_num):
                try:
                    t = self.instructions.time_array[i][j]
                    if t>0:
                        row = [i, j, time.strftime("%H:%M:%S", time.localtime(t))]
                        color = self.SpecRF.color_ij(self.instructions.loop_num, i, j)
                        # print(row, color)
                        text = "text_color" + str(i) + "_" + str(j)
                        tree.tag_configure(text, foreground=self.rgb_to_hex(color))
                        tree.insert("", tk.END, values=row, tags=(text,))
                except:
                    pass
                    # print(i,j, self.instructions.pos_num, self.instructions.loop_num)
        tree.place(x=0, y=0)

    def rgb_to_hex(self, rgb):
        r, g, b = rgb
        return "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))

    def highlight_row(self, tree, sel_index: int = 0):
        tree.tag_configure("highlight", background="yellow")

        n_rows = len(tree.get_children())
        for i in range(n_rows):
            item = tree.get_children()[i]
            current_tags = tree.item(item, "tags")
            new_tags = tuple(tag for tag in current_tags if tag != "highlight")
            tree.item(item, tags=new_tags)

        try:
            item = tree.get_children()[sel_index]
            tree.item(item, tags=("highlight",))
        except:
            pass
