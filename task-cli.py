import json # (Javascript Object Notation) -> Đọc, ghi, chuyển đổi dữ liệu giữa Python và file JSON(Văn bản) 
import os # (Operating System) -> Tương tác với hệ điều hành(Kiểm tra, thao tác/thư mục)
import sys # (System) -> Giúp tương tác qua Terminal
from datetime import datetime
FILENAME = "tasks.json" # File được lưu vào
VALID_STATUSTES = ["todo", "in-progress", "done"]
ts = datetime.now().strftime("%d-%m-%Y %H:%M:%S") # Chỉnh lại format thời gian

def load_tasks(): 
    """Đọc file JSON vả trả về danh sách tasks"""
    if not os.path.exists(FILENAME): # Kiểm tra nếu không tồn tại thì trả về rỗng
        return [] 
    try:
        with open(FILENAME, "r") as f: # Mở file ở chế độ đọc
            return json.load(f)  # Đọc dữ liệu JSON và chuyển thành list/dict
    except json.JSONDecodeError:
        print("Warning: tasks.json is corrupted. Starting fresh.")
        return []
    
def save_tasks(tasks):
    """Gởi danh sách tasks vào file JSON"""
    with open(FILENAME, "w") as f: # Mở file ở chế độ ghi
        json.dump(tasks, f, indent=2) # Ghi dữ liệu  vào file với indent = 2 

"""Thêm task mới"""    
def add_task(args, tasks):
    if len(args) < 3: 
        print("Error: Please provide a task description")
        return
    
    parts = args[2:] # Duyệt từ vị trí thứ 3 tới cuối 
    status = "todo" # Mặc định
    if parts[-1].lower() in VALID_STATUSTES:
        status = parts.pop().lower() # Lấy và sửa phần cuối
    
    title = " ".join(parts) # Lấy mô tả task
    new_id = len(tasks) + 1 # Tạo ID mới        
    createdAt = ts
    updatedAt = ts
    task = {"id": new_id, "title": title, "status": status, "createdAt": createdAt, "updateAt": updatedAt} # Tạo task mới
    tasks.append(task) # Thêm vào danh sách
    save_tasks(tasks) # Ghi lại file JSON
    print(f"Added task #{new_id}: {title}, time: {createdAt}, lastUpdate: {updatedAt}") # In ra thông báod
    
"""Hiển thị danh sách task"""
def list_task(args, tasks):
    if len(tasks) == 0: # Nếu độ dài của tasks = 0 thì danh sách rỗng
        print("The list is empty")
        return
    list_type = ""
    if len(args) >= 3:
        list_type = args[2] # Lấy status 
    else:
        print("[TASK LIST]") 
        for task in tasks:
            print(f'#{task["id"]}: {task["title"]} [{task["status"]}] [created: {task["createdAt"]}] [lastUpdate: {task["updateAt"]}]')
        return

    if list_type in VALID_STATUSTES:
        check = 0
        for task in tasks:
            if task["status"] == list_type:
                if check == 0:
                    print("[TASK LIST]")
                    check = 1
                print(f'#{task["id"]}: {task["title"]} [{task["status"]}] [created: {task["createdAt"]}] [lastUpdate: {task["updateAt"]}]')
        if check == 0:
            print("The list is empty")
    else:
        print("There is no type of list you're looking for")   

"""Cập nhật task(Mô tả)"""
def update_task(args, tasks):
    if len(args) < 4: # Nếu sau id không có gì thì báo lỗi
        print("Error: Please provide a task description")
        return
    task_found = 0
    selected_id = int(args[2]) # Chọn vị trí id
    for task in tasks:
        if task["id"] == selected_id:
            parts = args[3:] # Duyệt từ vị trí thứ 4 tới cuối 
            task_found = 1
            
            title = " ".join(parts)
            task["title"] = title
            task["updatedAt"] = ts
            break
    if task_found == 0: # Kiểm tra xem task có tôn tại không
        print("Update failed")
        return
    else:
        save_tasks(tasks)                     
        print("Update successfully")

"""Xóa task"""
def delete_task(args, tasks):
    if len(tasks) == 0: # Không có gì để xóa
        print("Error: Nothing to delete")
        return

    if len(args) < 3: # Báo lỗi nếu không nhập gì sau delete 
        print("Error: Please provide a task description")
        return

    selected_id = int(args[2]) # Ép chuôi sang kiểu só
    id = 0
    task_found = 0
    for task in tasks: # Xóa thông qua id
        if task["id"] == selected_id: 
            task_found = 1
            tasks.remove(task)
            break
    # Kiểm tra xem task có tồn tại không
    if task_found == 0:
        print("Delete failed")
    else:    
        for task in tasks: # Cập nhật lại thứ tự
            task["id"] = id + 1; id += 1 
        print("Delete successfully")
        save_tasks(tasks)
        
"""Cập nhật trạng thái của task"""
def mark_task(args, tasks, command):
    if len(args) < 3:
        print("Error: Please provide a description")
        return
    new_status = command.replace("mark-", "").lower() # Tách ra
    selected_id = int(args[2])
    task_found = 0
    if new_status not in VALID_STATUSTES: # Kiểm tra xem status có valid không
        print("Failed mark")
        return
    else:
        for task in tasks: # 
            if task["id"] == selected_id:
                task_found = 1
                task["status"] = new_status # Cập nhật trạng thái mới
                task["updatedAt"] = ts
                break
    if task_found == 0:
        print("Failed mark")
        return
    else:
        print("Successfully Mark")
        save_tasks(tasks)
        return
        
"""Hàm main chạy"""
def main():
    args = sys.argv # Lấy lệnh từ terminal ("Task-cli.py", "add", "Học Python")
    if len(args) < 2: # Nếu len < 2 có nghĩa là người dùng không nhập gì sau lệnh add 
        print("Usage: python task_tracker.py [add|list|update|delete|mark-done|mark-in-progres|mark-todo|clear]")
        return 
    
    command = args[1] # Lấy lệnh người dùng (add, list, delete...)
    tasks = load_tasks() # Đọc dữ liệu hiện tại từ file
    # Thêm
    if command == "add":
        add_task(args, tasks)
    # Show list
    elif command == "list":
        list_task(args, tasks)     
    # Update
    elif command == "update":
        update_task(args, tasks)
    # Xóa thông qua id
    elif command == "delete":
        delete_task(args, tasks)
    elif command.startswith("mark-"): # Kiểm tra bắt đầu từ
        mark_task(args, tasks, command)
    # Xoá toàn bộ danh sách 
    elif command == "clear":
        tasks.clear()
        save_tasks(tasks)
    else:
        print("Unknown command")
        
if __name__ == "__main__": # Hàm test 
    main()
    
    

