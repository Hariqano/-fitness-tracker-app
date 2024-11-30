import customtkinter as ctk
import json
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from customtkinter import CTkImage  # For improved image handling
from bcrypt import hashpw, gensalt, checkpw  # Secure password handling

class ExerciseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # App Configuration
        self.title("Exercise Tracker")
        self.geometry("800x600")
        self.user_data_file = "user_data.json"
        self.current_user = None

        # Initialize Data
        self.exercise_data = []
        self.exercise_image_path = None

        # Set Theme
        ctk.set_appearance_mode("System")  # Options: "Light", "Dark", "System"

        # Initialize Login Screen
        self.login_screen()

    # Utility Methods
    def create_label(self, parent, text, **kwargs):
        label = ctk.CTkLabel(parent, text=text, **kwargs)
        label.pack(pady=10)
        return label

    def create_entry(self, parent, placeholder="", password=False, **kwargs):
        entry = ctk.CTkEntry(parent, show="*" if password else "", placeholder_text=placeholder, **kwargs)
        entry.pack(pady=10)
        return entry

    def create_button(self, parent, text, command, **kwargs):
        button = ctk.CTkButton(parent, text=text, command=command, **kwargs)
        button.pack(pady=10)
        return button

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def load_user_data(self):
        if os.path.exists(self.user_data_file):
            try:
                with open(self.user_data_file, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Data file corrupted. Resetting user data.")
                return {}
        return {}

    def save_user_data(self, data):
        with open(self.user_data_file, "w") as file:
            json.dump(data, file)


    # Main app functions (previously defined, including BMR, TDEE, etc.)
    def calculate_bmr(self,weight, height, age, gender):
        if gender == "Male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        return bmr
    
    
    def calculate_tdee(self,bmr, activity_level):
        if activity_level == "Sedentary":
            tdee = bmr * 1.2
        elif activity_level == "Active":
            tdee = bmr * 1.55
        else:
            tdee = bmr * 1.725
        return tdee

    def calculate_macros(self,tdee, weight, goal, protein_factor=2.0, carb_factor=4.0, fat_factor=1.0):
        if goal == "Weight Loss":
            caloric_intake = tdee - 500
        elif goal == "Muscle Gain":
            caloric_intake = tdee + 300
        else:
            caloric_intake = tdee

        protein = weight * protein_factor
        protein_calories = protein * 4
        carbs = weight * carb_factor
        carbs_calories = carbs * 4
        fat = weight * fat_factor
        fat_calories = fat * 9

        total_calories = protein_calories + carbs_calories + fat_calories
        return caloric_intake, protein, carbs, fat, total_calories

    def display_results(self):
        try:
            age = int(self.entry_age.get())
            weight = float(self.entry_weight.get())
            height = int(self.entry_height.get())
            gender = self.gender_var.get()
            activity_level = self.activity_level_var.get()
            goal = self.goal_var.get()

            bmr = self.calculate_bmr(weight, height, age, gender)
            tdee = self.calculate_tdee(bmr, activity_level)
            caloric_intake, protein, carbs, fat, total_calories = self.calculate_macros(tdee, weight, goal)

            self.result_text = f"Your Total Daily Energy Expenditure (TDEE) is: {tdee:.2f} calories/day\n"
            self.result_text += f"Calories you should eat for {goal}: {caloric_intake:.2f} calories/day\n"
            self.result_text += f"Macronutrient Breakdown:\n"
            self.result_text += f"Protein: {protein:.2f} grams\n"
            self.result_text += f"Carbohydrates: {carbs:.2f} grams\n"
            self.result_text += f"Fat: {fat:.2f} grams\n"
            self.result_text += f"Total Calories from Macros: {total_calories:.2f} calories\n"

            self.label_result.configure(text=self.result_text)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values.")

    def show_main_app(self):
        # Inputs for main app
        self.label_age.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_age.grid(row=0, column=1, padx=10, pady=10)

        self.label_weight.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_weight.grid(row=1, column=1, padx=10, pady=10)

        self.label_height.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_height.grid(row=2, column=1, padx=10, pady=10)

        self.label_gender.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.radio_male.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.radio_female.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.label_activity.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.activity_level_menu.grid(row=5, column=1, padx=10, pady=10)

        self.label_goal.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.goal_menu.grid(row=6, column=1, padx=10, pady=10)

        # New Button for Calculating Daily Eat
        self.calculate_daily_button.grid(row=7, column=0, columnspan=2, pady=20)

        self.label_result.grid(row=8, column=0, columnspan=2, padx=10, pady=10)


    # Screens
    def login_screen(self):
        self.clear_window()
        self.title("Login")

        self.create_label(self, text="Login", font=("Arial", 20, "bold"))
        self.username_entry = self.create_entry(self, placeholder="Username")
        self.password_entry = self.create_entry(self, placeholder="Password", password=True)

        self.create_button(self, text="Login", command=self.login)
        self.create_button(self, text="Register", command=self.register_screen)

    def register_screen(self):
        self.clear_window()
        self.title("Register")

        self.create_label(self, text="Register", font=("Arial", 20, "bold"))
        self.new_username_entry = self.create_entry(self, placeholder="Username")
        self.new_password_entry = self.create_entry(self, placeholder="Password", password=True)
        self.confirm_password_entry = self.create_entry(self, placeholder="Confirm Password", password=True)

        self.create_button(self, text="Register", command=self.register)
        self.create_button(self, text="Back to Login", command=self.login_screen)

    def main_screen(self):
        self.clear_window()
        self.title(f"Exercise Tracker - {self.current_user}")


        # Scrollable Frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_label(self.scrollable_frame, text="This app helps you stay on track with your fitness goals.\n\n Features include:\n- Track your workouts\n- Calculate your daily calorie needs\n", font=("Arial", 20, "bold"))


        #Exercise screen
        self.create_label(self.scrollable_frame, text="You can now save your exercises and review!!", font=("Arial", 16, "bold"))
        self.create_button(self.scrollable_frame, text="Exercise", command=self.view_exercises)

        #calculate screen
        self.create_label(self.scrollable_frame, text="Click the button below to calculate your calorie needs!", font=("Arial", 16, "bold"))
        self.create_button(self.scrollable_frame, text="calculate calories!", command=self.Calculate_screen)

    def Calculate_screen(self):
        self.clear_window()

        # Main app layout (hidden initially)
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Inputs Section
        self.create_label(self.scrollable_frame , text="Age:", font=("Arial", 16, "bold"))
        self.entry_age = self.create_entry(self.scrollable_frame)



        self.create_label(self.scrollable_frame , text="Weight (kg):", font=("Arial", 16, "bold"))
        self.entry_weight =  self.create_entry(self.scrollable_frame)


        self.create_label(self.scrollable_frame , text="Height (cm):", font=("Arial", 16, "bold"))
        self.entry_height =  self.create_entry(self.scrollable_frame)


        # Gender selection
        self.create_label(self.scrollable_frame , text="Gender:", font=("Arial", 16, "bold"))
        self.gender_var = ctk.StringVar(value="")
        self.radio_male = ctk.CTkRadioButton(self.scrollable_frame, text="Male", variable=self.gender_var, value="Male").pack(pady=10)
        self.radio_female = ctk.CTkRadioButton(self.scrollable_frame, text="Female", variable=self.gender_var, value="Female").pack(pady=10)

        # Activity Level selection
        self.create_label(self.scrollable_frame , text="Activity Level:", font=("Arial", 16, "bold"))
        self.activity_level_var = ctk.StringVar(self.scrollable_frame,value="")
        self.activity_level_options = ["Sedentary", "Active", "Very Active"]
        self.activity_level_menu = ctk.CTkOptionMenu(self.scrollable_frame, variable=self.activity_level_var, values=self.activity_level_options).pack(pady=10)

        # Goal selection
        self.create_label(self.scrollable_frame , text="Goal:", font=("Arial", 16, "bold"))
        self.goal_var = ctk.StringVar(self.scrollable_frame,value="")
        self.goal_options = ["Weight Loss", "Muscle Gain", "Maintaining Weight"]
        self.goal_menu = ctk.CTkOptionMenu(self.scrollable_frame, variable=self.goal_var, values=self.goal_options).pack(pady=10)

        # Button to calculate (this is the new button)
        self.create_button(self.scrollable_frame, text="Calculate Your Daily Eat",command=self.display_results)


        # Result Display Section
        self.label_result =  self.create_label(self.scrollable_frame , text="", font=("Arial", 16, "bold"))

        self.create_button(self, text="Back", command=self.main_screen)



    def view_exercises(self):
        self.clear_window()

        # Scrollable Frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Input Fields
        self.create_label(self.scrollable_frame, text="Add Exercise", font=("Arial", 16, "bold"))
        self.exercise_name_entry = self.create_entry(self.scrollable_frame, placeholder="Exercise Name")
        self.weight_entry = self.create_entry(self.scrollable_frame, placeholder="Weight (kg)")

        self.create_button(self.scrollable_frame, text="Upload Image", command=self.upload_image)
        self.create_button(self.scrollable_frame, text="Save Exercise", command=self.save_exercise)

        self.create_button(self.scrollable_frame, text="View Previous Exercises", command=self.view_previous_exercises)

        self.create_button(self, text="Back", command=self.main_screen)


    

    # Functional Methods
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user_data = self.load_user_data()

        # Check if user exists and password matches (check salt validity)
        if username in user_data:
            stored_hash = user_data[username]["password"]

            # Ensure the password hash format is valid (bcrypt hashes begin with $2b$ or $2a$)
            if stored_hash.startswith("$2b$") or stored_hash.startswith("$2a$"):
                if checkpw(password.encode(), stored_hash.encode()):
                    self.current_user = username
                    self.exercise_data = user_data[username].get("exercise_data", [])
                    self.main_screen()
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password.")
            else:
                messagebox.showerror("Login Failed", "Stored password hash is invalid. Please reset your password.")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        user_data = self.load_user_data()

        if username in user_data:
            messagebox.showerror("Error", "Username already exists.")
            return

        # Hash the password and store the user data
        hashed_password = hashpw(password.encode(), gensalt())
        user_data[username] = {"password": hashed_password.decode(), "exercise_data": []}
        self.save_user_data(user_data)

        messagebox.showinfo("Registration Success", "Account created successfully.")
        self.login_screen()

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select a Machine Image",
                                               filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.exercise_image_path = file_path
            messagebox.showinfo("Image Uploaded", "Machine image uploaded successfully.")

    def save_exercise(self):
        exercise_name = self.exercise_name_entry.get()
        weight = self.weight_entry.get()

        if not exercise_name or not weight:
            messagebox.showerror("Missing Data", "Please fill in all fields.")
            return

        try:
            weight = float(weight)
        except ValueError:
            messagebox.showerror("Invalid Weight", "Weight must be a number.")
            return

        exercise = {"name": exercise_name, "weight": weight, "image": self.exercise_image_path}

        self.exercise_data.append(exercise)

        user_data = self.load_user_data()
        user_data[self.current_user]["exercise_data"] = self.exercise_data
        self.save_user_data(user_data)

        messagebox.showinfo("Success", "Exercise saved successfully.")
        self.view_previous_exercises()

    def view_previous_exercises(self):
        self.clear_window()
        self.title("Previous Exercises")

        # Scrollable Frame
        frame = ctk.CTkScrollableFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        for i, exercise in enumerate(self.exercise_data):
           

            self.create_label(frame, text=f"{exercise['name']} \n \n{exercise['weight']} kg", font=("Arial", 14))

            if exercise["image"]:
                try:
                    img = CTkImage(Image.open(exercise["image"]), size=(150, 150))
                    ctk.CTkLabel(frame, image=img, text="").pack(pady=10)
                    self.create_label(frame, text=f"--------------------------", font=("Arial", 14))
                except Exception:
                    self.create_label(frame, text="Error loading image")
        


        self.create_button(self, text="Back", command=self.view_exercises)

if __name__ == "__main__":
    app = ExerciseApp()
    app.mainloop()




