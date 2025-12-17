# 🧾 Todo List Manager (Python)
[![Python](https://img.shields.io/badge/Python-3.13.7-blue?logo=python&logoColor=white)](https://www.python.org/) [![Version](https://img.shields.io/badge/Version-2.5.0-orange)]() [![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT) [![Languages](https://img.shields.io/badge/Languages-English%20%7C%20German-blue)]()

A lightweight and easy-to-use **terminal-based Todo List Manager** built with Python.  
Create, manage, and save multiple todo lists — stored neatly in a `todos.json` file.  
**Available in English and German.**

---

## ✨ Features

✅ Create and manage **multiple todo lists**  
📝 Add, view, delete, clear, or **check/uncheck** todos  
📅 **Date tracking** for every todo (automatically saved)  
🎨 Improved todo display with **colored date output** in the terminal  
🔁 Todo check/uncheck system with **automatic JSON saving**  
⚙️ **Settings menu** to change app language & countdown timer  
💾 **Persistent storage** (`todos.json` + `settings.json`)  
⏱️ Adjustable **countdown delay** for UI feedback  
🖥️ Clean and user-friendly terminal interface  
⚠️ Comprehensive **error handling system**  
🔄 **Backward compatible** with old todos (todos without dates show `--.--.----`)

---

## 📝 Changelog

### **v2.5.0**
- feat: added **date tracking** for each todo item  
- feat: improved todo data structure (`text`, `date`, `done`)  
- feat: enhanced todo display with **colored date output**  
- feat: automatic migration support for old todos without dates  
- refactor: internal todo handling for better extensibility  

### **v2.4.1**
- fix: corrected display bug where the old main menu and settings menu in German were not shown correctly

### **v2.4.0**
- feat: added todo toggle (check/uncheck) functionality with persistent saving  
- feat: introduced settings menu to change language and countdown timer  
- feat: added configurable countdown delay for smoother UI feedback
