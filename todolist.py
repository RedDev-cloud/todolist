import json
import os

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
        "enter_number": "Gib die Nummer ein:",
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
        "menu_change_lang": "5 - Sprache ändern",
        "menu_exit": "6 - Programm beenden",

        # Todolisten-Menü
        "menu_todo": "Tippe:",
        "menu_add": "1 - Ein Todo hinzufügen",
        "menu_show": "2 - Alle Todos anzeigen",
        "menu_remove": "3 - Ein Todo löschen",
        "menu_clear": "4 - Alle Todos löschen",
        "menu_close": "5 - Todoliste schließen",
        "menu_exit_todo": "6 - Programm beenden",

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
        "error_6": "todos.json konnte nicht geladen werden!"
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
        "todolist_deleted": "Todolist '{name}' has been deleted!",
        "todolist_name": "What should the todolist be called?",
        "enter_number": "Enter the number:",
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
        "menu_change_lang": "5 - Change language",
        "menu_exit": "6 - Exit program",

        # Todo menu
        "menu_todo": "Type:",
        "menu_add": "1 - Add a todo",
        "menu_show": "2 - Show all todos",
        "menu_remove": "3 - Remove a todo",
        "menu_clear": "4 - Delete all todos",
        "menu_close": "5 - Close todolist",
        "menu_exit_todo": "6 - Exit program",

        "enter_todo": "What do you want to add?",
        "todos_empty": "You have no todos!",
        "todo_deleted": "\"{item}\" has been deleted!",
        "all_todos_deleted": "All todos have been deleted.",

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
# Funktionen
# =======================

def t(key, **kwargs):
    """Gibt die Übersetzung für den aktuellen Schlüssel zurück."""
    text = translations.get(language, {}).get(key, key)
    return text.format(**kwargs) if isinstance(text, str) else key


def save_todos(todos, list_name, file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[list_name] = todos

    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_todos(list_name):
    try:
        with open("todos.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(list_name, [])
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


def language_choice():
    global language
    loop = True
    if not language:
        language = "English"
    print(t("choose_language"))
    print(t("choose_option"))
    print("      1 - English")
    print("      2 - Deutsch")
    print("      3" + t("cancel"))
    choice = input("> ").strip()

    if choice == "1":
        language = "English"
    elif choice == "2":
        language = "Deutsch"
    elif choice == "3":
        return loop
    else:
        error(1, choice)
        return loop

    save_todos(language, "<language>", "settings.json")


def error(code, choice=None):
    """Zeigt einen Fehlertext aus dem Wörterbuch an."""
    print("\n>>>")
    print(f"   {t('error_header', code=code)}")
    print(f"   {t(f'error_{code}', choice=choice)}")
    print(">>>")
    print("")
    input(t("press_enter"))


# =======================
# Hauptprogramm
# =======================
todolist = False
todos = []
language = load_setting("<language>")
 
if not language:
    while True:
        clear_screen()
        loop = language_choice()
        if not loop:
            break


while True:
    clear_screen()
    # Menü anzeigen
    if todolist:
        print(f"Todoliste: {todolist}\n")
        print(t("menu_todo"))
        print("      " + t("menu_add"))
        print("      " + t("menu_show"))
        print("      " + t("menu_remove"))
        print("      " + t("menu_clear"))
        print("      " + t("menu_close"))
        print("      " + t("menu_exit_todo"))
    else:
        print(t("menu_main"))
        print("      " + t("menu_create"))
        print("      " + t("menu_open"))
        print("      " + t("menu_delete"))
        print("      " + t("menu_delete_all"))
        print("      " + t("menu_change_lang"))
        print("      " + t("menu_exit"))

    choice = input("> ").strip()
    clear_screen()

    # =======================
    # Todolisten-Modus
    # =======================
    if todolist:
        if choice == "1":
            newitem = input(t("enter_todo") + " ").strip()
            if not newitem:
                error(4, choice)
            else:
                todos.append(newitem)
                save_todos(todos, todolist, "todos.json")

        elif choice == "2":
            if todos:
                print("Todos:")
                for i, todo in enumerate(todos, start=1):
                    print(f"      {i}. {todo}")
                print("")
                input(t("press_enter"))
            else:
                error(3, choice)

        elif choice == "3":
            if not todos:
                error(3, choice)
                continue

            print(t("enter_number"))
            for i, todo in enumerate(todos, start=1):
                print(f"{i}. {todo}")
            choice_num = input("> ").strip()

            if not choice_num.isdigit():
                error(2, choice_num)
                continue

            num = int(choice_num)
            if 1 <= num <= len(todos):
                removed = todos.pop(num - 1)
                save_todos(todos, todolist, "todos.json")
                print(t("todo_deleted", item=removed))
                input(t("press_enter"))
            else:
                error(1, num)

        elif choice == "4":
            if todos:
                print(t("confirm_all_delete"))
                print(t("continue"))
                print("2" + t("cancel"))
                confirm = input("> ").strip()
                if confirm == "1":
                    todos.clear()
                    save_todos(todos, todolist, "todos.json")
                    print(t("all_todos_deleted"))
                    input(t("press_enter"))
                elif confirm == "2":
                    print(t("aborted"))
                    input(t("press_enter"))
                else:
                    error(1, confirm)
            else:
                error(3, choice)

        elif choice == "5":
            todolist = False
            todos = []

        elif choice == "6":
            break

        else:
            error(1, choice)

    # =======================
    # Hauptmenü
    # =======================
    else:
        if choice == "1":
            print(t("todolist_name"))
            newitem = input("> ").strip()
            if not newitem:
                error(4, choice)
            else:
                save_todos([], newitem, "todos.json")

        elif choice == "2":
            try:
                with open("todos.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                if data:
                    print("Welche Todoliste möchtest du öffnen?")
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

        elif choice == "3":
            try:
                with open("todos.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                if not data:
                    error(5, choice)
                    continue

                print("Welche Todoliste möchtest du löschen?")
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
                        input(t("press_enter"))
                    elif confirm == "2":
                        print(t("aborted"))
                        input(t("press_enter"))
                    else:
                        error(1, confirm)
                else:
                    error(1, choice_delete)

            except (FileNotFoundError, json.JSONDecodeError):
                error(6, choice)

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
                    input(t("press_enter"))
                elif confirm == "2":
                    print(t("aborted"))
                    input(t("press_enter"))
                else:
                    error(1, confirm)

            except (FileNotFoundError, json.JSONDecodeError):
                error(6, choice)

        elif choice == "5":
            language_choice()

        elif choice == "6":
            break

        else:
            error(1, choice)
