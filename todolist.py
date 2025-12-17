import json
import os
import time
from datetime import datetime

# ANSI-Farbcodes
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

# =======================
# Übersetzungs-System
# =======================
translations = {
    "Deutsch": {
        # Allgemeine Texte
        "choose_language": "In welcher Sprache soll dieses Programm sein?",
        "choose_option": "Tippe:",
        "press_enter": "Zum Fortfahren Enter drücken: ",
        "aborted": "Abgebrochen",
        "deleted_all": "Alle Todolisten wurden gelöscht!",
        "no_todolists": "Es wurden keine Todolisten gefunden!",
        "todolist_opened": "Todoliste '{name}' wurde geöffnet!",
        "todolist_deleted": "Todoliste '{name}' wurde gelöscht!",
        "todolist_name": "Wie soll die Todoliste heißen?",
        "choose_todolist": "Welche Todoliste möchtest du öffnen?",
        "choose_delete_todolist": "Welche Todoliste möchtest du löschen?",
        "todo_delete": "Welches Todo möchtest du löschen?",
        "todo_toggle": "Welches Todo möchtest du (ent-)abhaken?",
        "confirm_delete": "Möchtest du '{name}' wirklich löschen?",
        "confirm_all_delete": "Möchtest du wirklich alle Todolisten löschen?",
        "continue": "1 - Fortfahren",
        "cancel": " - Abbrechen",
        # Hauptmenü
        "menu_main": "Tippe:",
        "menu_create": "1 - Eine Todoliste erstellen",
        "menu_open": "2 - Eine Todoliste öffnen",
        "menu_delete": "3 - Eine Todoliste löschen",
        "menu_delete_all": "4 - Alle Todolisten löschen",
        "menu_settings": "5 - Einstellungen",
        "menu_exit": "6 - Programm beenden",
        # Einstellungen-Menü
        "menu_change_lang": "1 - Sprache ändern",
        "menu_change_coldown": "2 - Countdown-Zeit ändern",
        "menu_close_settings": "3 - Einstellungen schließen",
        "menu_exit_settings": "4 - Programm beenden",
        "menu_coldown": "Gib die neue Countdown-Zeit ein (in Sekunden):",
        # Todolisten-Menü
        "menu_add": "1 - Ein Todo hinzufügen",
        "menu_show": "2 - Alle Todos anzeigen",
        "menu_check": "3 - Ein Todo abhaken/entabhaken",
        "menu_remove": "4 - Ein Todo löschen",
        "menu_clear": "5 - Alle Todos löschen",
        "menu_close": "6 - Todoliste schließen",
        "menu_exit_todo": "7 - Programm beenden",
        "enter_todo": "Was möchtest du hinzufügen?",
        "todos_empty": "Du hast keine Todos!",
        "todo_deleted": "\"{item}\" wurde gelöscht!",
        "all_todos_deleted": "Alle Todos wurden gelöscht.",
        # Fehler
        "error_header": "Fehler_{code}:",
        "error_1": "Die Auswahlmöglichkeit ({choice}) gibt es nicht!",
        "error_2": "Die Eingabe ({choice}) ist keine Zahl!",
        "error_3": "Du hast keine Todos!",
        "error_4": "Leere Eingaben sind nicht erlaubt!",
        "error_5": "Es wurden keine Todolisten in todos.json gefunden!",
        "error_6": "todos.json konnte nicht geladen werden!",
    },
    "English": {
        # General texts
        "choose_language": "Which language should this program use?",
        "choose_option": "Type:",
        "press_enter": "Press Enter to continue: ",
        "aborted": "Canceled",
        "deleted_all": "All todolists were deleted!",
        "no_todolists": "No todolists were found!",
        "todolist_opened": "Todolist '{name}' has been opened!",
        "choose_todolist": "Which todolist would you like to open?",
        "choose_delete_todolist": "Which Todolist would you like to delete?",
        "todolist_deleted": "Todolist '{name}' has been deleted!",
        "todolist_name": "What should the todolist be called?",
        "todo_delete": "Which todo would you like to delete?",
        "todo_toggle": "Which todo would you like to (un)check?",
        "confirm_delete": "Do you really want to delete '{name}'?",
        "confirm_all_delete": "Do you really want to delete all todolists?",
        "continue": "1 - Continue",
        "cancel": " - Cancel",
        # Main menu
        "menu_main": "Type:",
        "menu_create": "1 - Create a todolist",
        "menu_open": "2 - Open a todolist",
        "menu_delete": "3 - Delete a todolist",
        "menu_delete_all": "4 - Delete all todolists",
        "menu_settings": "5 - Change settings",
        "menu_exit": "6 - Exit program",
        # Todo menu
        "menu_add": "1 - Add a todo",
        "menu_show": "2 - Show all todos",
        "menu_check": "3 - Check/uncheck a todo",
        "menu_remove": "4 - Remove a todo",
        "menu_clear": "5 - Delete all todos",
        "menu_close": "6 - Close todolist",
        "menu_exit_todo": "7 - Exit program",
        "enter_todo": "What do you want to add?",
        "todos_empty": "You have no todos!",
        "todo_deleted": "\"{item}\" has been deleted!",
        "all_todos_deleted": "All todos have been deleted.",
        # Settings menu
        "menu_change_lang": "1 - Change language",
        "menu_change_coldown": "2 - Change countdown timer",
        "menu_close_settings": "3 - Exit settings",
        "menu_exit_settings": "4 - Exit program",
        "menu_coldown": "Enter the new countdown time (in seconds):",
        # Errors
        "error_header": "Error_{code}:",
        "error_1": "The option ({choice}) is not available!",
        "error_2": "The input ({choice}) is not a number!",
        "error_3": "You have no todos!",
        "error_4": "Empty entries are not allowed!",
        "error_5": "No todolists were found in todos.json!",
        "error_6": "todos.json could not be loaded!"
    }
}

# =======================
# Hilfsfunktionen
# =======================
def t(key, **kwargs):
    text = translations.get(language, {}).get(key, key)
    return text.format(**kwargs) if isinstance(text, str) else key

def save_todos(todos, list_name, file):
    """
    Speichert den Wert 'todos' unter dem Schlüssel list_name in der Datei file.
    'todos' kann eine beliebige JSON-serialisierbare Struktur sein (auch Settings).
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    data[list_name] = todos
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_todos(list_name):
    """
    Lädt die Todos für list_name. Unterstützt alte Form (Liste von Strings)
    und neue Form (Liste von Dicts).
    Gibt eine Liste von Dicts zurück: {"text":..., "date":..., "done":...}
    """
    try:
        with open("todos.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        raw = data.get(list_name, [])
        normalized = []
        for item in raw:
            if isinstance(item, dict):
                text = item.get("text", "") if item.get("text", None) is not None else ""
                date = item.get("date", "--.--.----")
                done = bool(item.get("done", False))
                normalized.append({"text": text, "date": date, "done": done})
            elif isinstance(item, str):
                done = item.startswith("[x] ")
                text = item[4:] if done else item
                date = "--.--.----"
                normalized.append({"text": text, "date": date, "done": done})
            else:
                normalized.append({"text": str(item), "date": "--.--.----", "done": False})
        return normalized
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def load_setting(setting):
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(setting, None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def language_choice(first_choice):
    global language
    loop = True
    if not language:
        language = "English"
    print(t("choose_language"))
    print(t("choose_option"))
    print(" 1 - English")
    print(" 2 - Deutsch")
    if not first_choice:
        print(" 3" + t("cancel"))
    choice = input("> ").strip()
    if choice == "1":
        language = "English"
    elif choice == "2":
        language = "Deutsch"
    elif choice == "3" and not first_choice:
        return loop
    else:
        error(1, choice)
    save_todos(language, "<language>", "settings.json")
    return loop

def error(code, choice=None):
    print("\n>>>")
    print(f" {t('error_header', code=code)}")
    print(f" {t(f'error_{code}', choice=choice)}")
    print(">>>")
    print("")
    input(t("press_enter"))

def format_todo_display(todo, index=None):
    """
    Gibt den formatieren String zurück, bei dem nur das Datum gelb gefärbt ist.
    """
    done_prefix = f"{GREEN}[x]{RESET} " if todo.get("done") else f"{GREEN}[ ]{RESET} "
    text = todo.get("text", "")
    date = todo.get("date", "--.--.----")
    colored_date = f"{YELLOW}{date}{RESET}"
    idx = f"{index}. " if index is not None else ""
    return f"{idx}{done_prefix}{text} {colored_date}"

# =======================
# Hauptprogramm
# =======================
todolist = False
settings_menu = False
todos = []
language = load_setting("<language>")
coldown = load_setting("<coldown>")

if not language:
    while True:
        clear_screen()
        loop = language_choice(True)
        if not loop:
            break

if not coldown:
    coldown = 0.5

while True:
    clear_screen()
    if todolist:
        print(f"Todoliste: {todolist}\n")
        print(t("menu_main"))
        print(" " + t("menu_add"))
        print(" " + t("menu_show"))
        print(" " + t("menu_check"))
        print(" " + t("menu_remove"))
        print(" " + t("menu_clear"))
        print(" " + t("menu_close"))
        print(" " + t("menu_exit_todo"))
    elif settings_menu == True:
        print(t("menu_main"))
        print(" " + t("menu_change_lang"))
        print(" " + t("menu_change_coldown"))
        print(" " + t("menu_close_settings"))
        print(" " + t("menu_exit_settings"))
    else:
        print(t("menu_main"))
        print(" " + t("menu_create"))
        print(" " + t("menu_open"))
        print(" " + t("menu_delete"))
        print(" " + t("menu_delete_all"))
        print(" " + t("menu_settings"))
        print(" " + t("menu_exit"))

    choice = input("> ").strip()
    clear_screen()

    # =======================
    # Todolisten-Menü
    # =======================
    if todolist:
        # 1 - Add
        if choice == "1":
            print(t("enter_todo"))
            newitem = input("> ").strip()
            if not newitem:
                error(4, choice)
            else:
                Datum = datetime.now().strftime("%d.%m.%Y")
                todos.append({"text": newitem, "date": Datum, "done": False})
                save_todos(todos, todolist, "todos.json")

        # 2 - Show all todos
        elif choice == "2":
            if todos:
                print("Todos:")
                for i, todo in enumerate(todos, start=1):
                    print(" " + format_todo_display(todo, i))
                print("")
                input(t("press_enter"))
            else:
                error(3, choice)

        # 3 - Toggle check/uncheck
        elif choice == "3":
            if todos:
                print("Todos:")
                for i, todo in enumerate(todos, start=1):
                    print(" " + format_todo_display(todo, i))
                print("")
                print(t("todo_toggle"))
                choice_num = input("> ").strip()
                if not choice_num.isdigit():
                    error(2, choice_num)
                    continue
                num = int(choice_num)
                if 1 <= num <= len(todos):
                    current_todo = todos[num - 1]
                    if current_todo.get("done"):
                        todos[num - 1]["done"] = False
                        print(f'"{current_todo.get("text")}" wurde wieder geöffnet.')
                    else:
                        todos[num - 1]["done"] = True
                        print(f'"{current_todo.get("text")}" wurde abgehakt.')
                    save_todos(todos, todolist, "todos.json")
                    time.sleep(coldown)
                else:
                    error(1, num)
            else:
                error(3, choice)

        # 4 - Delete a todo
        elif choice == "4":
            if not todos:
                error(3, choice)
                continue
            print(t("todo_delete"))
            for i, todo in enumerate(todos, start=1):
                print(f"{i}. {todo.get('text')} {YELLOW}{todo.get('date','--.--.----')}{RESET}")
            choice_num = input("> ").strip()
            if not choice_num.isdigit():
                error(2, choice_num)
                continue
            num = int(choice_num)
            if 1 <= num <= len(todos):
                removed = todos.pop(num - 1)
                save_todos(todos, todolist, "todos.json")
                print(t("todo_deleted", item=removed.get("text")))
                time.sleep(coldown)
            else:
                error(1, num)

        # 5 - Clear all todos
        elif choice == "5":
            if todos:
                print(t("confirm_all_delete"))
                print(t("continue"))
                print("2" + t("cancel"))
                confirm = input("> ").strip()
                if confirm == "1":
                    todos.clear()
                    save_todos(todos, todolist, "todos.json")
                    print(t("all_todos_deleted"))
                    time.sleep(coldown)
                elif confirm == "2":
                    print(t("aborted"))
                    time.sleep(coldown)
                else:
                    error(1, confirm)
            else:
                error(3, choice)

        # 6 - Close todolist
        elif choice == "6":
            todolist = False
            todos = []

        # 7 - Exit program
        elif choice == "7":
            break

        else:
            error(1, choice)

    # =======================
    # Einstellungen-Menü
    # =======================
    elif settings_menu == True:
        if choice == "1":
            language_choice(False)
        elif choice == "2":
            print(t("menu_coldown"))
            eingabe = input("> ")
            try:
                coldown = float(eingabe)
                save_todos(coldown, "<coldown>", "settings.json")
            except ValueError:
                error(2, eingabe)
        elif choice == "3":
            settings_menu = False
        elif choice == "4":
            break
        else:
            error(1, choice)

    # =======================
    # Hauptmenü
    # =======================
    else:
        # 1 - Create a todolist
        if choice == "1":
            print(t("todolist_name"))
            newitem = input("> ").strip()
            if not newitem:
                error(4, choice)
            else:
                # initial leer: neue Liste als leere Liste (künftig Dict-Objekte)
                save_todos([], newitem, "todos.json")

        # 2 - Open a todolist
        elif choice == "2":
            try:
                with open("todos.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                if len(data) == 1:
                    todolist = list(data.keys())[0]
                    todos = load_todos(todolist)
                    print(t("todolist_opened", name=todolist))
                    time.sleep(coldown)
                elif data:
                    print(t("choose_todolist"))
                    listen_namen = list(data.keys())
                    for i, name in enumerate(listen_namen, start=1):
                        print(f"{i}. {name}")
                    choice_open = input("> ").strip()
                    if not choice_open.isdigit():
                        error(2, choice_open)
                        continue
                    idx = int(choice_open)
                    if 1 <= idx <= len(listen_namen):
                        todolist = listen_namen[idx - 1]
                        todos = load_todos(todolist)
                    else:
                        error(1, choice_open)
                else:
                    error(5, choice)
            except (FileNotFoundError, json.JSONDecodeError):
                error(6, choice)

        # 3 - Delete a todolist
        elif choice == "3":
            try:
                with open("todos.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not data:
                    error(5, choice)
                    continue
                print(t("choose_delete_todolist"))
                listen_namen = list(data.keys())
                for i, name in enumerate(listen_namen, start=1):
                    print(f"{i}. {name}")
                choice_delete = input("> ").strip()
                if not choice_delete.isdigit():
                    error(2, choice_delete)
                    continue
                idx = int(choice_delete)
                if 1 <= idx <= len(listen_namen):
                    list_name = listen_namen[idx - 1]
                    print(t("confirm_delete", name=list_name))
                    print(t("continue"))
                    print("2" + t("cancel"))
                    confirm = input("> ").strip()
                    if confirm == "1":
                        del data[list_name]
                        with open("todos.json", "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=4, ensure_ascii=False)
                        print(t("todolist_deleted", name=list_name))
                        time.sleep(coldown)
                    elif confirm == "2":
                        print(t("aborted"))
                        time.sleep(coldown)
                    else:
                        error(1, confirm)
                else:
                    error(1, choice_delete)
            except (FileNotFoundError, json.JSONDecodeError):
                error(6, choice)

        # 4 - Delete all todolists
        elif choice == "4":
            try:
                with open("todos.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not data:
                    error(5, choice)
                    continue
                print(t("confirm_all_delete"))
                print(t("continue"))
                print("2" + t("cancel"))
                confirm = input("> ").strip()
                if confirm == "1":
                    with open("todos.json", "w", encoding="utf-8") as f:
                        json.dump({}, f, indent=4, ensure_ascii=False)
                    print(t("deleted_all"))
                    time.sleep(coldown)
                elif confirm == "2":
                    print(t("aborted"))
                    time.sleep(coldown)
                else:
                    error(1, confirm)
            except (FileNotFoundError, json.JSONDecodeError):
                error(6, choice)

        # 5 - Settings
        elif choice == "5":
            settings_menu = True

        # 6 - Exit
        elif choice == "6":
            break

        else:
            error(1, choice)