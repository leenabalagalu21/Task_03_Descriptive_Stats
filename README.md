# Research Task 03 – Descriptive Statistics with Python, Pandas, and Polars

This project compares three different strategies for computing descriptive statistics on real-world social media datasets (Facebook ads, Facebook posts, and Twitter posts). The goal is to evaluate accuracy, performance, and ease of use using:
- Pure Python (no libraries)
- Pandas
- Polars

The project also includes visualizations to support narrative insights.

---

## 📁 Dataset

You’ll need the following files locally (not provided in the repo):
- `2024_fb_ads_president_scored_anon.csv`
- `2024_fb_posts_president_scored_anon.csv`
- `2024_tw_posts_president_scored_anon.csv`

---

## ⚙️ Instructions to Run the Code

1. **Install required libraries**  
   Make sure Python 3.8+ is installed, then run:
   pip install pandas polars matplotlib seaborn

2. **Run the scripts to display stats**
   python pure_python_stats.py     
   python pandas_stats.py         
   python polars_stats.py
    
4. **Run the visulization script**
   python visualizations.py

## reflective questions
1. **Was it a challenge to produce identical results?**
Yes, it was. The biggest challenge was that each library handles standard deviation and missing values a bit differently. For example, Pandas uses ddof=1 by default, while Polars and base Python use ddof=0. I had to make sure all three used the same formula to get matching results. I also had to clean some columns that had nested or null values so that all three approaches could process them consistently.

2. **Do you find one approach easier or more performant?**
Pandas was the easiest to use — the syntax is simple and it handles messy data quite well. Polars was the most performant by far; it processed large datasets much faster than the other two. Base Python was the hardest and slowest because everything had to be done manually.

3. **If you were coaching a junior data analyst, what approach would you recommend?**
I would recommend starting with Pandas. It’s well-documented, widely used, and beginner-friendly. Once they’re comfortable, they can try Polars if they need more performance. I’d only suggest using base Python to learn how the calculations work behind the scenes.

4. **Can coding AI like ChatGPT produce recommendations such as template code to jump start each approach?**
Yes, definitely. I used ChatGPT to help me get started with my Pandas and Polars scripts. It gave good starter code that I could build on. For base Python, it helped structure the logic, though I had to tweak a lot more myself.

5. **What default approach do these tools recommend when asked to produce descriptive statistics?**
ChatGPT usually recommends using Pandas and suggests df.describe() right away. That’s a good default for most use cases, especially when exploring a new dataset.

6. **Do you agree with these recommendations (why or why not)?**
Yes, I agree. Pandas is a great starting point because it’s easy to use and powerful enough for most tasks. The only downside is that it can be slower on large datasets — that’s where Polars is a better choice. But overall, Pandas is the right default for beginners and general analysis.
