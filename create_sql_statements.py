import uuid

# List of exercises for legs, chest, and shoulders
exercises = [
    # Leg exercises
    ("leg", "Squat", "A basic lower-body exercise to strengthen the legs.", 60, 4),
    ("leg", "Lunge", "A lower-body exercise that targets the quads and glutes.", 60, 3),
    ("leg", "Leg Press", "A machine-based exercise for building leg strength.", 90, 4),
    
    # Chest exercises
    ("chest", "Bench Press", "A chest exercise to build upper body strength.", 90, 4),
    ("chest", "Chest Fly", "An isolation exercise for the chest muscles.", 60, 3),
    ("chest", "Push Up", "A bodyweight exercise for chest and upper body.", 45, 4),
    
    # Shoulder exercises
    ("shoulders", "Overhead Press", "A shoulder exercise to build strength.", 90, 4),
    ("shoulders", "Lateral Raise", "An isolation exercise for shoulder muscles.", 60, 3),
    ("shoulders", "Front Raise", "A front deltoid isolation exercise.", 60, 3)
]

# Generate SQL INSERT statements
for muscle, name, description, rest_period, sets in exercises:
    exercise_id = str(uuid.uuid4())  # Generate UUID
    sql_statement = f"""INSERT INTO exercises (id, target_muscle, name, description, rest_period_in_seconds, sets) VALUES ('{exercise_id}', '{muscle}', '{name}', '{description}', {rest_period}, {sets});"""
    print(sql_statement)
