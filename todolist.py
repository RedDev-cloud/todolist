import json
import os

def save_todos(todos, list_name):
    try:
        with open("todos.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Die entsprechende Liste aktualisieren oder neu anlegen
    data[list_name] = todos

    with open("todos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_todos(list_name):
    try:
        with open("todos.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(list_name, [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    
def error_1(Auswahl):
    print("")
    print(">>>")
    print("   Error_1:")
    print(f"   Die Auswahlmöglichkeit ({Auswahl}) gibt es nicht!")
    print(">>>")
    print("")
    input("Zum fortfahren Enter drücken: ")

def error_2(Auswahl):
    print("")
    print(">>>")
    print("   Error_2:")
    print(f"   Die Eingabe ({Auswahl}) ist keine Zahl!")
    print(">>>")
    print("")
    input("Zum fortfahren Enter drücken: ")

def error_3():
    print("")
    print(">>>")
    print("   Error_3:")
    print(f"   Du hast keine Todos!")
    print(">>>")
    print("")
    input("Zum fortfahren Enter drücken: ")

def error_4():
    print("")
    print(">>>")
    print("   Error_4:")
    print(f"   Leere Eingaben sind nicht erlaubt!")
    print(">>>")
    print("")
    input("Zum fortfahren Enter drücken: ")

def error_5():
    print("")
    print(">>>")
    print("   Error_4:")
    print("   Es wurden keine Todolisten in todos.json gefunden!")
    print(">>>")
    print("")
    input("Zum fortfahren Enter drücken: ")

def error_6():
    print("")
    print(">>>")
    print("   Error_4:")
    print("   todos.json konnte nicht geladen werden!")
    print(">>>")
    print("")
    input("Zum fortfahren Enter drücken: ")

todolist   = False
todos      = []

while True:
    clear_screen()

    if todolist:
        print(f"Todoliste: {todolist}")
        print("")
        print("Tippe:")
        print("      1 - Ein Todo hinzufügen")
        print("      2 - Alle Todos anzeigen")
        print("      3 - Ein Todo löschen")
        print("      4 - Alle Todos löschen")
        print("      5 - Todoliste schließen")
        print("      6 - Programm beenden")
    else:
        print("Tippe:")
        print("      1 - Eine Todoliste erstellen")
        print("      2 - Eine Todolist öffnen")
        print("      3 - Eine Todoliste löschen")
        print("      4 - Alle Todolisten löschen")
        print("      5 - Programm beenden")
    
    newitem_or_read = input("> ")
    clear_screen()

    if todolist:
        if newitem_or_read == "1":
            print("Was möchtest du hinzufügen? ")
            newitem = input("> ").strip()
            if not newitem:
                error_4()
            else:
                todos.append(newitem)
                save_todos(todos, todolist)

        elif newitem_or_read == "2":
            if todos:
                print("Todos:")
                for i, todo in enumerate(todos, start=1):
                    print(f"      {i}. {todo}")
                print("")
                input("Zum fortfahren Enter drücken: ")

            else:
                error_3()

        elif newitem_or_read == "3":
            if not todos:
                error_3()
                continue

            print("Welche Todo möchtest du löschen?")
            for i, todo in enumerate(todos, start=1):
                print(f"{i}. {todo}")

            try:
                Auswahl = (input("> Gib die Nummer ein: "))
                num = int(Auswahl)
                if 1 <= num <= len(todos):
                    entfernt = todos.pop(num - 1)
                    save_todos(todos, todolist)
                    print("")
                    print(f'"{entfernt}" wurde gelöscht!')
                    print("")
                    input("Zum fortfahren Enter drücken: ")
                else:
                    error_1(num)
            except ValueError:
                error_2(Auswahl)

        elif newitem_or_read == "4":
            if todos:
                print("Möchtest du wirklich alle Todos löschen?")
                print("Tippe:")
                print("      1 - Fortfahren")
                print("      2 - Abbrechen")
                question = input("> ")
        
                if question == "1":
                    todos.clear()
                    save_todos(todos, todolist)
                    print("")
                    print("Alle Todos wurden gelöscht.")
                    print("")
                    input("Zum fortfahren Enter drücken: ")
                elif question == "2":
                    print("")
                    print("Abgebrochen")
                    print("")
                    input("Zum fortfahren Enter drücken: ")
                else:
                    error_1(question)
            else:
                error_3()

        elif newitem_or_read == "5":
            todolist = False
            todos    = []

        elif newitem_or_read == "6":
            break
        else:
            error_1(newitem_or_read)
    
    else:
        if newitem_or_read == "1":
            print("Wie soll die Todoliste heißen?")
            newitem = input("> ").strip()
            if not newitem:
                error_4()
            else:
                save_todos(todos, newitem)
        
        elif newitem_or_read == "2":
            try:
                with open("todos.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                    if data:
                        print("Welche Todoliste möchtest du öffnen?")

                        listen_namen = list(data.keys())
                        for i, name in enumerate(listen_namen, start=1):
                            print(f"{i}. {name}")

                        print("")
                        Auswahl = input("> Gib die Nummer ein: ").strip()

                        if not Auswahl.isdigit():
                            error_2(Auswahl)
                            continue

                        Auswahl = int(Auswahl)

                        # Prüfen, ob Zahl im gültigen Bereich liegt
                        if 1 <= Auswahl <= len(listen_namen):
                            todolist = listen_namen[Auswahl - 1]
                            todos = load_todos(todolist)
                            print("")
                            print(f"Todoliste '{todolist}' wurde geöffnet!")
                        else:
                            error_1(Auswahl)

                    else:
                        error_5()

            except (FileNotFoundError, json.JSONDecodeError):
                error_6()

        elif newitem_or_read == "3":
            try:    
                with open("todos.json", "r", encoding="utf-8") as f:
                    data = json.load(f)

                if not data:
                    error_5()
                    continue

                print("Welche Todoliste möchtest du löschen?")
                listen_namen = list(data.keys())
                for i, name in enumerate(listen_namen, start=1):
                    print(f"{i}. {name}")

                print("")
                Auswahl = input("> Gib die Nummer ein: ").strip()

                if not Auswahl.isdigit():
                    error_2(Auswahl)
                    continue

                Auswahl = int(Auswahl)
                if 1 <= Auswahl <= len(listen_namen):
                    list_name = listen_namen[Auswahl - 1]
                    print("")
                    print(f"Möchtest du '{list_name}' wirklich löschen?")
                    print("Tippe:")
                    print("      1 - Fortfahren")
                    print("      2 - Abbrechen")
                    confirm = input("> ").strip()

                    if confirm == "1":
                        del data[list_name]
                        with open("todos.json", "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=4, ensure_ascii=False)
                        print("")
                        print(f"Todoliste '{list_name}' wurde gelöscht!")
                        print("")
                        input("Zum fortfahren Enter drücken: ")

                    elif confirm == "2":
                        print("")
                        print("Löschen abgebrochen.")
                        print("")
                        input("Zum fortfahren Enter drücken: ")

                    else:
                        error_1(confirm)
                else:
                    error_1(Auswahl)

            except (FileNotFoundError, json.JSONDecodeError):
                error_6()


        elif newitem_or_read in ("5", "6"):
            break
        
        else:
            error_1(newitem_or_read)