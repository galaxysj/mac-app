import tkinter as tk
import subprocess
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter import filedialog as fd
import os
import threading
from tkinter import simpledialog
import time
from time import sleep
from tkinter import messagebox






def update_label(text):
    label.config(text=text)
    label.update_idletasks()  # 글자 바뀐 후 실제 너비 반영
    w = label.winfo_width()
    root_w = root.winfo_width()
    label.place(x=(root_w - w)//2, y=45)

# ===================== start 관련 =====================
def start_thread():
    def task():
        apps_to_delete = [
            "com.android.vending",
            "com.sec.android.app.samsungapps",
            "com.kt.olleh.storefront",
            "com.skt.skaf.A000Z00040",
            "com.lguplus.appstore",
            "com.google.android.youtube",
            "com.android.chrome",
            "com.google.android.gm",
            "com.google.android.apps.maps",
            "com.google.android.googlequicksearchbox",
            "com.google.android.apps.tachyon",
            "com.sec.android.app.sbrowser",
            "com.sec.android.app.shealth",
            "com.sec.android.app.fm",
            "com.samsung.android.arzone",
            "com.samsung.android.themestore",
            "com.samsung.android.app.watchmanager",
            "com.samsung.android.voc",
            "com.samsung.android.oneconnect",
            "com.samsung.android.bixby.agent",
            "com.samsung.sec.android.prd",
            "com.sec.penup",
            "com.google.android.apps.photos",
            "com.google.android.videos",
            "com.google.android.apps.docs",
            "com.google.android.apps.youtube.music",
            "com.samsung.android.app.spage",
            "com.samsung.sree",
            "com.microsoft.skydrive",
            "com.microsoft.office.outlook",
            "com.microsoft.office.officehubrow",
            "com.google.android.apps.bard"
        ]

        total_steps = 4 + len(apps_to_delete)  # 다운로드 2 + 압축해제 1 + ./adb 시작 1 + 앱 삭제 갯수

        current_step = 0

        def update_progress():
            nonlocal current_step
            current_step += 1
            percent = (current_step / total_steps) * 100
            root.after(0, lambda: progress.config(value=percent))

        root.after(0, lambda: progress.config(mode="determinate", maximum=100, value=0))
        root.after(0, lambda: update_label('파일 다운로드 중...'))

        try:
            
            
            
            subprocess.run(f"cd platform-tools && ./adb start-server", shell=True)
            update_progress()

            root.after(0, lambda: update_label("앱 삭제 중..."))
    
            for package in apps_to_delete:
                subprocess.run(f'cd platform-tools && ./adb shell pm uninstall -k --user 0 {package}', shell=True)
                update_progress()
                root.update_idletasks()
                time.sleep(0.1)

        except Exception as e:
            root.after(0, lambda e=e: showerror("오류", f"{e}"))
        finally:
            root.after(0, lambda: progress.config(value=100))
            root.after(0, lambda: showinfo("안내", "삭제가 완료되었습니다."))
            root.after(0, lambda: update_label("준비"))

    threading.Thread(target=task, daemon=True).start()









# ===================== 무선start 관련 =====================
    
def wifistart():
    
    paddr = simpledialog.askstring(title="주소", prompt="페어링 IP와 포트를 입력하세요.")
    code = simpledialog.askstring(title="코드", prompt="페어링 코드를 입력하세요.")
    if not paddr or not code:
        showerror("오류", "IP 또는 페어링 코드가 입력되지 않았습니다.")
        return
    def task(paddr, code):
        apps_to_delete = [
            "com.android.vending",
            "com.sec.android.app.samsungapps",
            "com.kt.olleh.storefront",
            "com.skt.skaf.A000Z00040",
            "com.lguplus.appstore",
            "com.google.android.youtube",
            "com.android.chrome",
            "com.google.android.gm",
            "com.google.android.apps.maps",
            "com.google.android.googlequicksearchbox",
            "com.google.android.apps.tachyon",
            "com.sec.android.app.sbrowser",
            "com.sec.android.app.shealth",
            "com.sec.android.app.fm",
            "com.samsung.android.arzone",
            "com.samsung.android.themestore",
            "com.samsung.android.app.watchmanager",
            "com.samsung.android.voc",
            "com.samsung.android.oneconnect",
            "com.samsung.android.bixby.agent",
            "com.samsung.sec.android.prd",
            "com.sec.penup",
            "com.google.android.apps.photos",
            "com.google.android.videos",
            "com.google.android.apps.docs",
            "com.google.android.apps.youtube.music",
            "com.samsung.android.app.spage",
            "com.samsung.sree",
            "com.microsoft.skydrive",
            "com.microsoft.office.outlook",
            "com.microsoft.office.officehubrow",
            "com.google.android.apps.bard",
            "com.samsung.android.app.omcage"
        ]

        total_steps = 5 + len(apps_to_delete)  # 다운로드 2 + 압축해제 1 + ./adb 시작 1 + 앱 삭제 갯수

        current_step = 0

        def update_progress():
            nonlocal current_step
            current_step += 1
            percent = (current_step / total_steps) * 100
            root.after(0, lambda: progress.config(value=percent))

        root.after(0, lambda: progress.config(mode="determinate", maximum=100, value=0))
        root.after(0, lambda: update_label('파일 다운로드 중...'))

        try:
            
            subprocess.run(f"cd platform-tools && ./adb start-server", shell=True)
            update_progress()


            root.after(0, lambda: update_label("앱 삭제 중..."))
            subprocess.run(
                f'cd platform-tools && ./adb pair {paddr}',
                input=code + "\n",
                text=True,
                shell=True
            )
            sleep(10)
            
            update_progress()
            for package in apps_to_delete:
                subprocess.run(f'cd platform-tools && ./adb shell pm uninstall -k --user 0 {package}', shell=True)
                update_progress()
                root.update_idletasks()
                time.sleep(0.1)
                
            subprocess.run(f'cd platform-tools && ./adb disconnect && ./adb kill-server', shell=True)

        except Exception as e:
            root.after(0, lambda e=e: showerror("오류", f"{e}"))
        finally:
            root.after(0, lambda: progress.config(value=100))
            root.after(0, lambda: showinfo("안내", "삭제가 완료되었습니다."))
            root.after(0, lambda: update_label("준비"))

    threading.Thread(target=task, args=(paddr, code), daemon=True).start()
# ===================== recover 관련 =====================
def recover_thread():
    def task():
        apps_to_recover = [
            "com.android.vending",
            "com.sec.android.app.samsungapps",
            "com.kt.olleh.storefront",
            "com.skt.skaf.A000Z00040",
            "com.lguplus.appstore",
            "com.google.android.youtube",
            "com.android.chrome",
            "com.google.android.gm",
            "com.google.android.apps.maps",
            "com.google.android.googlequicksearchbox",
            "com.google.android.apps.tachyon",
            "com.sec.android.app.sbrowser",
            "com.sec.android.app.shealth",
            "com.sec.android.app.fm",
            "com.samsung.android.arzone",
            "com.samsung.android.themestore",
            "com.samsung.android.app.watchmanager",
            "com.samsung.android.voc",
            "com.samsung.android.spay",
            "com.samsung.android.oneconnect",
            "com.samsung.android.bixby.agent",
            "com.samsung.sec.android.prd",
            "com.sec.penup",
            "com.google.android.apps.photos",
            "com.google.android.videos",
            "com.google.android.apps.docs",
            "com.google.android.apps.youtube.music",
            "com.samsung.android.app.spage",
            "com.samsung.sree",
            "com.microsoft.skydrive",
            "com.microsoft.office.outlook",
            "com.microsoft.office.officehubrow",
            "com.google.android.apps.bard",
            "com.samsung.android.app.omcage"
        ]

        total_steps = 4 + len(apps_to_recover)  # 다운로드 2 + 압축해제 1 + ./adb 시작 1 + 복구 갯수

        current_step = 0

        def update_progress():
            nonlocal current_step
            current_step += 1
            percent = (current_step / total_steps) * 100
            root.after(0, lambda: progress.config(value=percent))

        root.after(0, lambda: progress.config(mode="determinate", maximum=100, value=0))
        root.after(0, lambda: update_label('파일 다운로드 중...'))

        try:
            
            
            subprocess.run(f"cd platform-tools && ./adb start-server", shell=True)
            update_progress()


            root.after(0, lambda: update_label("복구 중..."))
            
            for package in apps_to_recover:
                subprocess.run(f'cd platform-tools && ./adb shell pm install-existing --user 0 {package}', shell=True)
                update_progress()
                root.update_idletasks()
                time.sleep(0.1)
            subprocess.run(f'cd platform-tools && ./adb disconnect && ./adb kill-server', shell=True)

        except Exception as e:
            root.after(0, lambda e=e: showerror("오류", f"{e}"))
        finally:
            root.after(0, lambda: progress.config(value=100))
            root.after(0, lambda: showinfo("안내", "복구가 완료되었습니다."))
            root.after(0, lambda: update_label("준비"))

    threading.Thread(target=task, daemon=True).start()
#와이파이 복구
def wifirec():
    
    paddr = simpledialog.askstring(title="주소", prompt="페어링 IP와 포트를 입력하세요.")
    code = simpledialog.askstring(title="코드", prompt="페어링 코드를 입력하세요.")
    if not paddr or not code:
        showerror("오류", "IP 또는 페어링 코드가 입력되지 않았습니다.")
        return
    def task(paddr, code):
        apps_to_recover = [
            "com.android.vending",
            "com.sec.android.app.samsungapps",
            "com.kt.olleh.storefront",
            "com.skt.skaf.A000Z00040",
            "com.lguplus.appstore",
            "com.google.android.youtube",
            "com.android.chrome",
            "com.google.android.gm",
            "com.google.android.apps.maps",
            "com.google.android.googlequicksearchbox",
            "com.google.android.apps.tachyon",
            "com.sec.android.app.sbrowser",
            "com.sec.android.app.shealth",
            "com.sec.android.app.fm",
            "com.samsung.android.arzone",
            "com.samsung.android.themestore",
            "com.samsung.android.app.watchmanager",
            "com.samsung.android.voc",
            "com.samsung.android.spay",
            "com.samsung.android.oneconnect",
            "com.samsung.android.bixby.agent",
            "com.samsung.sec.android.prd",
            "com.sec.penup",
            "com.google.android.apps.photos",
            "com.google.android.videos",
            "com.google.android.apps.docs",
            "com.google.android.apps.youtube.music",
            "com.samsung.android.app.spage",
            "com.samsung.sree",
            "com.microsoft.skydrive",
            "com.microsoft.office.outlook",
            "com.microsoft.office.officehubrow",
            "com.google.android.apps.bard",
            "com.samsung.android.app.omcage"
        ]
        
        
        total_steps = 5 + len(apps_to_recover)  # 다운로드 2 + 압축해제 1 + ./adb 시작 1 + 복구 갯수

        current_step = 0

        def update_progress():
            nonlocal current_step
            current_step += 1
            percent = (current_step / total_steps) * 100
            root.after(0, lambda: progress.config(value=percent))

        root.after(0, lambda: progress.config(mode="determinate", maximum=100, value=0))
        root.after(0, lambda: update_label('파일 다운로드 중...'))

        try:
            
            
            subprocess.run(f"cd platform-tools && ./adb start-server", shell=True)
            update_progress()

            


            root.after(0, lambda: update_label("복구 중..."))
            subprocess.run(
                f'cd platform-tools && ./adb pair {paddr}',
                input=code + "\n",
                text=True,
                shell=True
            )
            sleep(10)
            
            update_progress()
            for package in apps_to_recover:
                subprocess.run(f'cd platform-tools && ./adb shell pm install-existing --user 0 {package}', shell=True)
                update_progress()
                root.update_idletasks()
                time.sleep(0.1)
            subprocess.run(f'cd platform-tools && ./adb disconnect && ./adb kill-server', shell=True)

        except Exception as e:
            root.after(0, lambda e=e: showerror("오류", f"{e}"))
        finally:
            root.after(0, lambda: progress.config(value=100))
            root.after(0, lambda: showinfo("안내", "복구가 완료되었습니다."))
            root.after(0, lambda: update_label("준비"))

    threading.Thread(target=task, args=(paddr, code), daemon=True).start()
# ===================== install 관련 =====================

def install_app_thread():
    filename = fd.askopenfilename()
    if not filename:
        return

    def task():
        total_steps = 6
        current_step = 0
        def update_progress():
            nonlocal current_step
            current_step += 1
            percent = (current_step / total_steps) * 100
            root.after(0, lambda: progress.config(value=percent))

        root.after(0, lambda: progress.config(mode="determinate", maximum=100, value=0))
        root.after(0, lambda: update_label('파일 준비 중...'))

        try:
            fixed_path = filename
            filename_only = os.path.basename(fixed_path)
            temp_file = fixed_path + ".apk"

            # 파일명 변경 (원본 덮어쓰지 않도록 주의)
            os.rename(fixed_path, temp_file)
            update_progress()



            
            subprocess.run(f"cd platform-tools && ./adb start-server", shell=True)
            update_progress()

            root.after(0, lambda: update_label('설치 중...'))
            subprocess.run(r'cd platform-tools && ./adb install "' + temp_file + '"', shell=True)
            update_progress()

            # 원래 이름으로 복원
            os.rename(temp_file, fixed_path)

        except Exception as e:
            root.after(0, lambda: showerror("오류", f"설치 중 오류 발생:\n{e}"))

        finally:
            root.after(0, lambda: progress.config(value=100))
            root.after(0, lambda: showinfo("안내", '설치가 완료되었습니다.'))
            root.after(0, lambda: update_label('준비'))

    threading.Thread(target=task, daemon=True).start()
def wifiitl():
    
    paddr = simpledialog.askstring(title="주소", prompt="페어링 IP와 포트를 입력하세요.")
    code = simpledialog.askstring(title="코드", prompt="페어링 코드를 입력하세요.")
    if not paddr or not code:
        showerror("오류", "IP 또는 페어링 코드가 입력되지 않았습니다.")
        return
    filename = fd.askopenfilename()
    if not filename:
        return

    def task(paddr, code):
        total_steps = 6
        current_step = 0
        def update_progress():
            nonlocal current_step
            current_step += 1
            percent = (current_step / total_steps) * 100
            root.after(0, lambda: progress.config(value=percent))

        root.after(0, lambda: progress.config(mode="determinate", maximum=100, value=0))
        root.after(0, lambda: update_label('파일 준비 중...'))

        try:
            fixed_path = filename
            filename_only = os.path.basename(fixed_path)
            temp_file = fixed_path + ".apk"

            # 파일명 변경 (원본 덮어쓰지 않도록 주의)
            os.rename(fixed_path, temp_file)
            update_progress()



            root.after(0, lambda: update_label('설치 중...'))
            subprocess.run(
                f'cd platform-tools && ./adb pair {paddr}',
                input=code + "\n",
                text=True,
                shell=True
            )
            sleep(10)
            
            update_progress()
            
            subprocess.run(r'cd platform-tools && ./adb install "' + temp_file + '"', shell=True)
            update_progress()
            subprocess.run(f'cd platform-tools && ./adb disconnect && ./adb kill-server', shell=True)

            # 원래 이름으로 복원
            os.rename(temp_file, fixed_path)

        except Exception as e:
            root.after(0, lambda: showerror("오류", f"설치 중 오류 발생:\n{e}"))

        finally:
            root.after(0, lambda: progress.config(value=100))
            root.after(0, lambda: showinfo("안내", '설치가 완료되었습니다.'))
            root.after(0, lambda: update_label('준비'))

    threading.Thread(target=task, args=(paddr, code), daemon=True).start()
# ===================== 무선연결 관련  =====================
def changewifi():
    cng_btn.config(text="유선", command=changeusb)
    start_btn.config(text="무선 시작", command=wifistart)
    recover_btn.config(text="무선 복구", command=wifirec)
    study_btn.config(text="무선 설치", command=wifiitl)
    mul_btn.config(command=manualwifi)
def changeusb():
    cng_btn.config(text="무선", command=changewifi)
    start_btn.config(text="유선 시작", command=start_thread)
    recover_btn.config(text="유선 복구", command=recover_thread)
    study_btn.config(text="유선 설치", command=install_app_thread)
    mul_btn.config(command=manual)
# ================== 여러 줄 입력 다이얼로그 ==================
def multiline_input(title="입력", prompt="삭제할 패키지를 줄 단위로 입력하세요."):
    dialog = tk.Toplevel()
    dialog.title(title)

    tk.Label(dialog, text=prompt).pack(padx=10, pady=5)

    text = tk.Text(dialog, width=50, height=15)
    text.pack(padx=10, pady=5)

    result = {"value": None}

    def on_ok():
        result["value"] = text.get("1.0", tk.END).strip()
        dialog.destroy()

    tk.Button(dialog, text="확인", command=on_ok).pack(pady=5)
    dialog.grab_set()
    dialog.wait_window()
    return result["value"]
#===============체크파일===========================



def checkfile():
    def task():
        folder_path = "platform-tools"
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            print("폴더가 존재합니다.")
            buttons = [study_btn, recover_btn, cng_btn, start_btn]
            for b in buttons:
                b.config(state="disabled")
            update_label("준비 중...")
            subprocess.run('cd platform-tools && ./adb devices', shell=True)
            subprocess.run('cd platform-tools && ./adb kill-server', shell=True)
            update_label("준비")
            for b in buttons:
                b.config(state="normal")
        else:
            showinfo("안내", '실행을 위한 파일이 없어 다운로드를 진행합니다. 확인을 누를 시 다운로드가 시작됩니다.')
            buttons = [study_btn, recover_btn, cng_btn, start_btn]
            for b in buttons:
                b.config(state="disabled")
        
            steps = [
                ('다운로드 중...', 'curl -L -o platform-tools-latest-darwin.zip https://dl.google.com/android/repository/platform-tools-latest-darwin.zip'),
                ('압축해제 중...', 'unzip platform-tools-latest-darwin.zip'),
                ('실행권한 얻는 중...', 'cd platform-tools && chmod +x ./adb')
            ]

            total_steps = len(steps)
            current_step = 0

            for desc, cmd in steps:
                update_label(desc)
                subprocess.run(cmd, shell=True)
                current_step += 1
                percent = (current_step / total_steps) * 100
                root.after(0, lambda p=percent: progress.config(value=p))
                time.sleep(0.1)  # GUI 갱신 대기
                
            subprocess.run('cd platform-tools && ./adb devices', shell=True)
            subprocess.run('cd platform-tools && ./adb kill-server', shell=True)

            update_label("준비")
            root.after(0, lambda: progress.config(value=0))
            for b in buttons:
                b.config(state="normal")

    threading.Thread(target=task, daemon=True).start()

def manual():
    packages = multiline_input("수동 삭제", "삭제할 패키지를 줄 단위로 입력하세요.")
    if not packages:
        return

    package_list = packages.splitlines()

    def task(package_list):
        try:
            root.after(0, lambda: update_label('삭제 중...'))
            for package in package_list:
                if package.strip():
                    print("삭제:", package)
                    subprocess.run(f'cd platform-tools && ./adb shell pm uninstall -k --user 0 {package.strip()}', shell=True)
            subprocess.run(f'cd platform-tools && ./adb disconnect && ./adb kill-server', shell=True)
        finally:
            root.after(0, lambda: update_label('준비'))

    threading.Thread(target=task, args=(package_list,), daemon=True).start()


#=================수동무선========================
def manualwifi():
    paddr = simpledialog.askstring(title="주소", prompt="페어링 IP와 포트를 입력하세요.")
    code = simpledialog.askstring(title="코드", prompt="페어링 코드를 입력하세요.")
    packages = multiline_input("수동 삭제", "삭제할 패키지를 줄 단위로 입력하세요.")
    if not paddr or not code or not packages:
        messagebox.showerror("오류", "입력값이 부족합니다.")
        return

    package_list = packages.splitlines()

    def task(package_list):
        try:
            root.after(0, lambda: update_label('삭제 중...'))
            subprocess.run(
                f'cd platform-tools && ./adb pair {paddr}',
                input=code + "\n",
                text=True,
                shell=True
            )
            sleep(10)

            for package in package_list:
                if package.strip():
                    print("삭제:", package)
                    subprocess.run(f'cd platform-tools && ./adb shell pm uninstall -k --user 0 {package.strip()}', shell=True)

            subprocess.run(f'cd platform-tools && ./adb disconnect && ./adb kill-server', shell=True)
        finally:
            root.after(0, lambda: update_label('준비'))

    threading.Thread(target=task, args=(package_list,), daemon=True).start()
    
#===============기본설정=================
root = tk.Tk()
root.title("학습폰 5.0 for macOS")
root.geometry("400x150")
root.configure(bg="white")

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", maximum=100, value=0)
progress.place(x=50, y=70)
label = tk.Label(root, text="준비", bg="white")
label.place(x=180, y=45)

study_btn = tk.Button(root, text="유선 설치", command=install_app_thread, width=10, height=1, font=("Segoe UI", 9), bg="white")
study_btn.place(x=15, y=110)

recover_btn = tk.Button(root, text="유선 복구", command=recover_thread, width=10, height=1, font=("Segoe UI", 9), bg="white")
recover_btn.place(x=305, y=110)

start_btn = tk.Button(root, text="유선 시작", command=start_thread, width=10, height=1, font=("Segoe UI", 9), bg="white")
start_btn.place(x=215, y=110)

cng_btn = tk.Button(root, text="무선", command=changewifi, width=5, height=1, font=("Segoe UI", 9), bg="white")
cng_btn.place(x=10, y=10)

mul_btn = tk.Button(root, text="수동", command=manual, width=5, height=1, font=("Segoe UI", 9), bg="white")
mul_btn.place(x=341, y=10)

root.after(100, checkfile)


root.mainloop()




