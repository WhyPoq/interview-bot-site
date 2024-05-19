import os
import shutil
import json
import html

QUESTION_DIR = "questions"
SITE_RES_DIR = "site_resources"
WEBSITE_DIR = "website"

def copy_dir(source_dir, destination_dir):
	# Create the destination directory if it doesn't exist
	if not os.path.exists(destination_dir):
		os.makedirs(destination_dir)

	# Iterate over all items in the source directory
	for item in os.listdir(source_dir):
		source_item = os.path.join(source_dir, item)
		destination_item = os.path.join(destination_dir, item)

		# Check if it is a directory
		if os.path.isdir(source_item):
			# Recursively copy the subdirectory
			copy_dir(source_item, destination_item)
		else:
			# Copy the file
			shutil.copy2(source_item, destination_item)

def generate_categories_page():
	file_content = """\
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>Темы для собеседований</title>

		<meta
			name="description"
			content="Все доступные темы с вопросами для подготовки к собеседованию"
		/>
		<meta
			name="keywords"
			content="темы, все темы, категории, все категории, собеседование, interview bot, интервью бот"
		/>

		<link rel="icon" type="image/x-icon" href="/Assets/favicon.ico" />

		<link rel="preconnect" href="https://fonts.googleapis.com" />
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
		<link
			href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=Roboto+Mono:ital,wght@0,100..700;1,100..700&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap"
			rel="stylesheet"
		/>

		<link rel="stylesheet" href="/common.css" />
		<link rel="stylesheet" href="categories.css" />
	</head>
	<body>
		<header>
			<div class="main-page-link">
				<a href="/" aria-label="Перейти на главную страницу">
					<div class="main-page-link-logo">
						<img src="/Assets/logo_small.webp" alt="Логотип interview bot" />
					</div>
				</a>
				<p>Interview bot</p>
			</div>
		</header>
		<main>
			<h1>Вопросы для собеседований по темам:</h1>
			<ul>
"""
	# Iterate over all categories
	for category_filename in os.listdir(QUESTION_DIR):
		with open(os.path.join(QUESTION_DIR, category_filename), "r", encoding='utf-8') as f:
			category_data = json.load(f)
			category_name = " ".join(category_data["category_human_form"].split("_"))
			file_content += f"""\
				<li><a href="./{html.escape(category_data["category_filename_form"])}.html">{html.escape(category_name)}</a></li>
"""
		
	file_content += """\
			</ul>
		</main>
	</body>
</html>\
"""
	with open(os.path.join(WEBSITE_DIR, "categories", "index.html"), "w", encoding="utf-8") as f:
		f.write(file_content)

# ================================================================================================
# ================================================================================================
# ================================================================================================

def generate_category_page(category_data_filename):
	with open(os.path.join(QUESTION_DIR, category_data_filename), "r", encoding='utf-8') as f:
		category_data = json.load(f)
		category_raw_filename = category_data["category_filename_form"]
		category_questions = category_data["questions"]
		category_split = category_data["category_human_form"].split("_")
		if(len(category_split) == 1):
			category_main_name = None
			position_name = category_split[0]
		else:
			category_main_name = category_split[-1]
			position_name = " ".join(category_split[:-1])

	file_content = """\
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
"""

	if(category_main_name != None):
		file_content += f"""\
		<title>{html.escape(category_main_name)} топ {len(category_questions)} вопросов для {html.escape(position_name)} на собеседовании</title>
		<meta
			name="description"
			content="Часто задаваемые вопросы с правильными ответами на собеседовании на позицию {html.escape(position_name)} по теме {html.escape(category_main_name)}"
		/>
"""
	else:
		file_content += f"""\
		<title>топ {len(category_questions)} вопросов для {html.escape(position_name)} на собеседовании</title>
		<meta
			name="description"
			content="Часто задаваемые вопросы с правильными ответами на собеседовании на позицию {html.escape(position_name)}"
		/>
"""
		
	full_split_reversed = category_data["category_full_form"].split("_")
	full_split_reversed.reverse()
	keywords = ", ".join(full_split_reversed)
	h1_text = " ".join(category_data["category_human_form"].split("_"))

	file_content += f"""\
		<meta
			name="keywords"
			content="{html.escape(keywords)}, подготовка к собеседованию, вопросы для собеседования, вопросы на собеседование, собеседование, интервью, interview bot, интервью бот"
		/>

		<link rel="icon" type="image/x-icon" href="/Assets/favicon.ico" />

		<link rel="preconnect" href="https://fonts.googleapis.com" />
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
		<link
			href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=Roboto+Mono:ital,wght@0,100..700;1,100..700&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap"
			rel="stylesheet"
		/>

		<link rel="stylesheet" href="/common.css" />
		<link rel="stylesheet" href="questions.css" />
	</head>
	<body>
		<header class="main-page-link">
			<a href="/" aria-label="Перейти на главную страницу">
				<div class="main-page-link-logo">
					<img src="/Assets/logo_small.webp" alt="Логотип interview bot" />
				</div>
			</a>
			<p>Interview bot</p>
		</header>
		<main>
			<h2>Вопросы для собеседования на тему</h2>
			<h1>{html.escape(h1_text)}</h1>

			<ol>
"""
	
	for question in category_questions:
		question_text = question["question"]
		right_answer = question["right_answer"]
		file_content += f"""\
				<li>
					<h3>{html.escape(question_text)}</h3>
					<p>{html.escape(right_answer)}</p>
				</li>
"""
	file_content += f"""\
			</ol>
		</main>

		<footer>
			<p class="more-question">
				Больше вопросов у нашего
				<a class="telegram-bot-link" href="https://t.me/interview_training_bot"
					>телеграм бота</a
				>
			</p>
			<p>
				Там вы можете отвечать на вопросы голосовыми сообщениями и нейронная сеть проверит
				ваш ответ и даст фидбэк
			</p>
		</footer>
	</body>
</html>

"""
	with open(os.path.join(WEBSITE_DIR, "categories", f"{category_raw_filename}.html"), "w", encoding="utf-8") as f:
		f.write(file_content)

# ================================================================================================
# ================================================================================================
# ================================================================================================

def generate():
	if not os.path.exists(QUESTION_DIR):
		raise Exception(f"Directory for questions '{QUESTION_DIR}' does not exist")
	
	if not os.path.exists(SITE_RES_DIR):
		raise Exception(f"Directory for site resources '{SITE_RES_DIR}' does not exist")
	
	if not os.path.exists(WEBSITE_DIR):
		os.makedirs(WEBSITE_DIR)

	# copy all site resources
	copy_dir(SITE_RES_DIR, WEBSITE_DIR)

	generate_categories_page()
	
	# generate pages for all categories
	
	site_categories_path = os.path.join(WEBSITE_DIR, "categories")
	if not os.path.exists(site_categories_path):
		os.makedirs(site_categories_path)

	# Iterate over all categories
	for category_filename in os.listdir(QUESTION_DIR):
		generate_category_page(category_filename)



if __name__ == "__main__":
	generate()