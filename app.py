import streamlit as st
import pandas as pd
import io

def round_to_nearest_plate(weight):
    return round(weight / 5) * 5

def calculate_max(weight, reps):
    try:
        weight = float(weight)
        reps = int(reps)
        if reps == 1:
            return weight
        return round(weight * (1 + (0.0333 * reps)), 2)
    except ValueError:
        return 0.0

def generate_juggernaut_program(bench_max, squat_max, deadlift_max):
    training_max = {
        "Bench": bench_max,
        "Squat": squat_max,
        "Deadlift": deadlift_max
    }

    waves = {
        "10s": [60, 70, 75],
        "8s": [60, 75, 80],
        "5s": [70, 75, 80, 85],
        "3s": [75, 80, 85, 90]
    }

    wave_structure = {
        "10s": [(4, 10), (3, 10), (1, 10), (3, 5)],
        "8s": [(4, 8), (3, 8), (1, 8), (3, 5)],
        "5s": [(5, 5), (3, 5), (1, 5), (3, 5)],
        "3s": [(6, 3), (3, 3), (1, 3), (3, 5)]
    }

    deload_percentages = [40, 50, 60]

    week_3_reps = {
        "10s": [(60, 3), (70, 1), (75, 10)],
        "8s": [(60, 3), (75, 1), (80, 8)],
        "5s": [(70, 2), (75, 2), (80, 1), (85, 5)],
        "3s": [(75, 1), (80, 1), (85, 1), (90, 3)]
    }

    program_data = []

    for wave in waves:
        for week in range(1, 5):
            if week != 3:
                sets, reps = wave_structure[wave][week - 1]
                rep_set_format = f"{reps} x {sets}"

                if week == 4:
                    bench_weight = round_to_nearest_plate(training_max["Bench"] * (deload_percentages[1] / 100))
                    squat_weight = round_to_nearest_plate(training_max["Squat"] * (deload_percentages[1] / 100))
                    deadlift_weight = round_to_nearest_plate(training_max["Deadlift"] * (deload_percentages[1] / 100))
                else:
                    bench_weight = round_to_nearest_plate(training_max["Bench"] * (waves[wave][week - 1] / 100))
                    squat_weight = round_to_nearest_plate(training_max["Squat"] * (waves[wave][week - 1] / 100))
                    deadlift_weight = round_to_nearest_plate(training_max["Deadlift"] * (waves[wave][week - 1] / 100))

                program_data.append({
                    "Wave": wave,
                    "Week": f"Week {week}",
                    "Reps x Sets": rep_set_format,
                    "Bench (lbs)": int(bench_weight),
                    "Squat (lbs)": int(squat_weight),
                    "Deadlift (lbs)": int(deadlift_weight)
                })
            else:
                for rep_set in week_3_reps[wave]:
                    rep_set_format = f"{rep_set[0]}% x {rep_set[1]} reps"
                    bench_weight = round_to_nearest_plate(training_max["Bench"] * (rep_set[0] / 100))
                    squat_weight = round_to_nearest_plate(training_max["Squat"] * (rep_set[0] / 100))
                    deadlift_weight = round_to_nearest_plate(training_max["Deadlift"] * (rep_set[0] / 100))

                    program_data.append({
                        "Wave": wave,
                        "Week": "Week 3",
                        "Reps x Sets": rep_set_format,
                        "Bench (lbs)": int(bench_weight),
                        "Squat (lbs)": int(squat_weight),
                        "Deadlift (lbs)": int(deadlift_weight)
                    })

    return pd.DataFrame(program_data)

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

st.set_page_config(page_title="Juggernaut Training Program", page_icon="🏋️", layout="wide")

st.title("Juggernaut Training Program Generator")
st.markdown("### Build your personalized strength training program")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Your 1RM")
    st.markdown("Enter your **1 Rep Max** for each lift:")
    
    input_method = st.radio("Input Method:", ["Direct 1RM", "Calculate from Weight x Reps"], horizontal=True)
    
    if input_method == "Direct 1RM":
        bench_max = st.number_input("Bench Press 1RM (lbs)", min_value=0, value=225, step=5)
        squat_max = st.number_input("Squat 1RM (lbs)", min_value=0, value=315, step=5)
        deadlift_max = st.number_input("Deadlift 1RM (lbs)", min_value=0, value=405, step=5)
    else:
        st.markdown("**Bench Press**")
        bench_col1, bench_col2 = st.columns(2)
        with bench_col1:
            bench_weight = st.number_input("Weight (lbs)", min_value=0, value=200, step=5, key="bench_weight")
        with bench_col2:
            bench_reps = st.number_input("Reps", min_value=1, value=5, step=1, key="bench_reps")
        bench_max = calculate_max(bench_weight, bench_reps)
        st.info(f"Estimated 1RM: **{bench_max:.0f} lbs**")
        
        st.markdown("**Squat**")
        squat_col1, squat_col2 = st.columns(2)
        with squat_col1:
            squat_weight = st.number_input("Weight (lbs)", min_value=0, value=275, step=5, key="squat_weight")
        with squat_col2:
            squat_reps = st.number_input("Reps", min_value=1, value=5, step=1, key="squat_reps")
        squat_max = calculate_max(squat_weight, squat_reps)
        st.info(f"Estimated 1RM: **{squat_max:.0f} lbs**")
        
        st.markdown("**Deadlift**")
        deadlift_col1, deadlift_col2 = st.columns(2)
        with deadlift_col1:
            deadlift_weight = st.number_input("Weight (lbs)", min_value=0, value=365, step=5, key="deadlift_weight")
        with deadlift_col2:
            deadlift_reps = st.number_input("Reps", min_value=1, value=5, step=1, key="deadlift_reps")
        deadlift_max = calculate_max(deadlift_weight, deadlift_reps)
        st.info(f"Estimated 1RM: **{deadlift_max:.0f} lbs**")

with col2:
    st.subheader("Your Training Maxes")
    st.markdown("---")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Bench", f"{bench_max:.0f} lbs")
    with metric_col2:
        st.metric("Squat", f"{squat_max:.0f} lbs")
    with metric_col3:
        st.metric("Deadlift", f"{deadlift_max:.0f} lbs")
    
    st.markdown("---")
    st.markdown("### About Juggernaut Method")
    st.markdown("""
    The Juggernaut Method is a 16-week strength program divided into four 4-week waves:
    - **10s Wave**: Build volume and work capacity
    - **8s Wave**: Increase intensity while maintaining volume
    - **5s Wave**: Focus on strength development
    - **3s Wave**: Peak strength and power
    
    Each wave includes 3 weeks of progressive overload followed by a deload week.
    """)

st.divider()

if st.button("Generate My Program", type="primary", use_container_width=True):
    if bench_max > 0 and squat_max > 0 and deadlift_max > 0:
        st.success("Program generated successfully!")
        
        df = generate_juggernaut_program(bench_max, squat_max, deadlift_max)
        
        st.subheader("Your Complete 16-Week Program")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Full Program", "10s Wave", "8s Wave", "5s Wave", "3s Wave"])
        
        with tab1:
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Wave": st.column_config.TextColumn("Wave", width="small"),
                    "Week": st.column_config.TextColumn("Week", width="small"),
                    "Reps x Sets": st.column_config.TextColumn("Reps x Sets", width="medium"),
                    "Bench (lbs)": st.column_config.NumberColumn("Bench (lbs)", format="%d"),
                    "Squat (lbs)": st.column_config.NumberColumn("Squat (lbs)", format="%d"),
                    "Deadlift (lbs)": st.column_config.NumberColumn("Deadlift (lbs)", format="%d"),
                }
            )
        
        for idx, wave in enumerate(["10s", "8s", "5s", "3s"], start=2):
            with [tab2, tab3, tab4, tab5][idx-2]:
                wave_df = df[df["Wave"] == wave].copy()
                wave_df = wave_df.drop(columns=["Wave"])
                
                st.dataframe(
                    wave_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Week": st.column_config.TextColumn("Week", width="small"),
                        "Reps x Sets": st.column_config.TextColumn("Reps x Sets", width="medium"),
                        "Bench (lbs)": st.column_config.NumberColumn("Bench (lbs)", format="%d"),
                        "Squat (lbs)": st.column_config.NumberColumn("Squat (lbs)", format="%d"),
                        "Deadlift (lbs)": st.column_config.NumberColumn("Deadlift (lbs)", format="%d"),
                    }
                )
        
        st.divider()
        
        csv = convert_df_to_csv(df)
        st.download_button(
            label="Download Program as CSV",
            data=csv,
            file_name="juggernaut_program.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.error("Please enter valid 1RM values for all lifts!")

st.divider()
st.markdown("---")
st.markdown("*Built with Streamlit | Train hard, train smart*")
