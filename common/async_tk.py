## async_tk
### common/async_tk.py
def async_run_with_loop(root, loop):
    def poll_loop():
        loop.call_soon(loop.stop)
        loop.run_forever()
        root.after(100, poll_loop)

    root.after(100, poll_loop)
    root.mainloop()

