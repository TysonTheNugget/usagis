from flask import Flask, render_template, jsonify
import os
import random
import re
from PIL import Image

app = Flask(__name__)

def index():
    fight_code = ""  # Initialize empty fight_code
    return render_template('index.html', fight_code=fight_code)

name_to_char = {
    # First 11 consonants
    'fury.10atk.3def.png': 'P',
    'ghost.7atk.6def.png': 'Q',
    'LeftRight.6atk.6def.png': 'R',
    'LoveStory.9atk.3def.png': 'S',
    'mecha.11atk.1def.png': 'T',
    'rip.9atk.7def.png': 'V',
    'squad.7atk.4def.png': 'W',
    'suingcompanies.7atk.5def.png': 'X',
    'sword.9atk.4def.png': 'Y',
    'uzi.7atk.6def.png': 'Z',
    'winged.5atk.10def.png': 'b',

    # Next 4 vowels
    'body1': 'oo',
    'body2': 'E',
    'body3': 'I',
    'body4': 'A',

    # Next 11 consonants
    'bit.7def.png': 'B',
    'bitballs.5atk.png': 'C',
    'bitship.2atk.2def.png': 'D',
    'bitwarrior.6atk.2def.png': 'F',
    'ice.7def.2atk.png': 'G',
    'ipad.5atk.5def.png': 'H',
    'reaper.5atk.3def.png': 'J',
    'risingbunny.3atk.7def.png': 'K',
    'rock.11def.png': 'L',
    'tcg.8atk.4def.png': 'M',
    'TIA.11atk.png': 'N',

    # Next 7 vowels
    'bunny.250speed.png': 'U',
    'content.220speed.png': 'a',
    'fang.210speed.png': 'e',
    'maniac2.200speed.png': 'ii',
    'open.225speed.png': 'o',
    'sad.215speed.png': 'u',
    'smirk.251speed.png': 'aa',

    # Next 7 consonants
    'Bigeyes.4def.2atk.png': 'c',
    'bushygreens.5atk.20speed.png': 'd',
    'Deadders.3atk.7def.png': 'f',
    'mad.7atk.10speed.png': 'g',
    'Majin.11atk.3def.5speed.png': 'h',
    'serious.12def.png': 'j',
    'sketchy.7atk.7.def.7speed.png': 'k',

    # Remaining vowels (not enough to fill all)
    'UI.60speed.png': 'y',
    'AppleVR.Gains 20 atk but only for the first 3 turns.png': 'ee',
    'BigGlasses.At start of battle if enemy atk is higher decrease their defense by 15. If lower increase this card atk by 7.png': 'i',
    'biggy.decreases own defense by 5 and increases attack by 12 for the rest of battle.png': 'AA',
    'BitWarriorHelm.increase hp by 300 when hp reaches 500 .When paired with bitwarrior increase the atk of this card by 20 on turn 5.png': '7',
    'Blueomb.when attacked enemy loses 1 atk and 1 def.png': 'uu',
    'BlueSunglass.enemy ordinal effect is negated.10def.10atk.png': '@',
    'Glasses.280hp.7def.png': '3',
    'Greenomb.every time this ordinal attacks increase its own atk and def by 1.png': '4',
    'karatekid2.when hp is below 500 this ordinal gains 55 atk.7def.png': 'yy',
    'OOP.on the 3rd turn flip a coin if heads increase atk by 20 if tails decrease def by 10.7atk.5def.20speed.png': '1',
    'Redomb.can attack twice on 4th turn.10atk.10def.png': 'O',
    'X.Each time this ordinal is attacked  10 times next 3 attacks will do 30 more  atk.10def.png': '0'
}



def extract_stats_from_filename(filename):
    stats = {}
    atk_match = re.search(r'(\d+)atk', filename)
    def_match = re.search(r'(\d+)def', filename)
    speed_match = re.search(r'(\d+)speed', filename)
    hp_match = re.search(r'(\d+)hp', filename)
    if atk_match:
        stats['ATK'] = int(atk_match.group(1))
    if def_match:
        stats['DEF'] = int(def_match.group(1))
    if speed_match:
        stats['SPEED'] = int(speed_match.group(1))
    if hp_match:  # New line
        stats['HP'] = int(hp_match.group(1))
    return stats

def extract_effect_from_filename(filename):
    base_name = os.path.splitext(filename)[0]
    parts = base_name.split('.')
    parts.pop(0)
    parts = [part for part in parts if not re.match(r'\d+(atk|def|speed)', part)]
    effect_text = ".".join(parts)
    
    # Debug: Print the effect_text to see if it's extracted correctly
    print("Debug: Extracted Effect Text:", effect_text)
    
    return effect_text

def format_filename_for_display(filename):
    base_name = os.path.splitext(filename)[0]
    stats_parts = re.findall(r'(\.\d+[atk|def|speed]+)', base_name)
    stats_text = ' '.join(['+' + s.lstrip('.') for s in stats_parts])
    formatted_name = re.sub(r'(\.\d+[atk|def|speed]+)', '', base_name).split('.')[0]
    return f"{formatted_name} {stats_text}"

def select_random_image_from_directory(directory, exclude=None):
    return random.choice([f for f in os.listdir(directory) if f.endswith('.png') and f != exclude])

def generate_random_color_background(width, height):
    color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
    return Image.new('RGB', (width, height), color)

def adjust_transparency(img):
    r, g, b, a = img.split()
    pixels = a.load()
    width, height = a.size
    for x in range(width):
        for y in range(height):
            if 0 < pixels[x, y] < 255:
                pixels[x, y] = 254
    return Image.merge('RGBA', (r, g, b, a))

def combine_images(layers):
    base = layers[0].convert('RGBA')
    for img_path in layers[1:]:
        img = Image.open(img_path).convert('RGBA')
        if 'Layer2' in img_path:
            img = adjust_transparency(img)
        base.paste(img, (0, 0), mask=img)
    return base

import os

import os  # Make sure to import os if it's not already imported

import os  # Make sure to import os at the beginning of your script

# Paste this modified function into your existing code.
def generate_simple_fight_code(background, body, boost, mouth, eyes, face, mapping):
    # Debug: Check the values of the arguments
    print("Debug: Arguments received by generate_simple_fight_code:")
    print(f"Background: {background}, Body: {body}, Boost: {boost}, Mouth: {mouth}, Eyes: {eyes}, Face: {face}")

    # Clean up the paths to match with dictionary keys
    background = os.path.basename(background)
    # For body, it's already a folder name; no need to clean it up
    boost = os.path.basename(boost)
    mouth = os.path.basename(mouth)
    eyes = os.path.basename(eyes)
    face = os.path.basename(face)

    # Debug: Check the cleaned-up values
    print("Debug: Cleaned-up arguments:")
    print(f"Cleaned Background: {background}, Cleaned Body: {body}, Cleaned Boost: {boost}, Cleaned Mouth: {mouth}, Cleaned Eyes: {eyes}, Cleaned Face: {face}")

    # Generate the fight code based on the mapping
    fight_code = ''.join([mapping.get(background, ''),
                      mapping.get(body.lower(), ''),  # Convert to lowercase here
                      mapping.get(boost, ''),
                      mapping.get(mouth, ''),
                      mapping.get(eyes, ''),
                      mapping.get(face, '')])

    # Debug: Check the generated fight code
    print("Debug: Generated Fight Code:", fight_code)

    return fight_code




def get_random_images():
    base_dir = 'base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')'
    layer_dirs = [
        'Layer1',
        ['Layer2/Body1', 'Layer2/Body2', 'Layer2/Body3', 'Layer2/Body4'],
        'Layer3',
        'Layer4',
        'Layer5',
        'Layer6'
    ]

    # Initialization
    selected_images = [generate_random_color_background(315, 240)]
    image_names = {}
    total_stats = {"ATK": 0, "DEF": 0, "SPEED": 0, "HP": 0}
    effect_text = ""
    bun_pb_holdings = ""
    exclude_from_layer6 = None

    # Debug: Inserting the debug line here, right after the initialization
    print("Debug: Initial image_names:", image_names)
    print("Debug: name_to_char mapping:", name_to_char)
    print("Debug: Starting image selection...")

    # Properly indented 'for' loop
    for layer in layer_dirs:
        if isinstance(layer, list):
            img_path = os.path.join(base_dir, random.choice(layer))
            print(f"Debug: Selected body directory: {img_path}")  # Debug line
            body_name_part = os.path.basename(img_path)
            image_names["Body"] = body_name_part
        else:
            img_path = os.path.join(base_dir, layer)

        selected_img = select_random_image_from_directory(img_path)
        if not selected_img:
            print(f"Warning: No image selected for {img_path}")
            continue

        if not isinstance(layer, list):
            formatted_name = format_filename_for_display(selected_img)
            image_names[layer] = formatted_name


        selected_images.append(os.path.join(img_path, selected_img))
        current_stats = extract_stats_from_filename(selected_img)
        total_stats['ATK'] += current_stats.get('ATK', 0)
        total_stats['DEF'] += current_stats.get('DEF', 0)
        total_stats['SPEED'] += current_stats.get('SPEED', 0)
        if "Body1" in img_path:  # This line and the following lines should be aligned properly
            total_stats['HP'] += 1000
        elif "Body2" in img_path:
            total_stats['HP'] += 1200
        elif "Body3" in img_path:
            total_stats['HP'] += 1100
        elif "Body4" in img_path:
            total_stats['HP'] += 1300
        if layer == 'Layer6':
            face_stats = extract_stats_from_filename(selected_img)  # New line
            total_stats['HP'] += face_stats.get('HP', 0)
            effect_text = extract_effect_from_filename(selected_img)
            print("Debug: Extracted Effect Text:", effect_text)
    
    if len(selected_images) < 6:
        print(f"Error: Not enough images selected. Only got {len(selected_images)} images.")
        return None

    fight_code = generate_simple_fight_code(
        selected_images[1].split('/')[-1],  # background
        image_names.get('Body', ''),         # body folder
        selected_images[3].split('/')[-1],   # boost
        selected_images[4].split('/')[-1],   # mouth
        selected_images[5].split('/')[-1],   # eyes
        selected_images[6].split('/')[-1],   # face
        name_to_char
    )

    print("Debug: fight_code inside get_random_images:", fight_code)
    return selected_images, image_names, total_stats, effect_text, bun_pb_holdings, fight_code




@app.route('/')
def index():
    return render_template('index.html')
@app.route('/beta')
def beta():
    return render_template('index2.html')
@app.route('/randomize', methods=['POST'])
def randomize_image():
    try:
        selected_images, image_names, total_stats, effect_text, bun_pb_holdings, fight_code = get_random_images()
        combined_image = combine_images(selected_images)
        combined_image_path = "static/randomized_image.png"
        combined_image.save(combined_image_path)
        print("Fight Code:", fight_code)
        print("Debug: Sending fightCode:", fight_code)         
        return jsonify({
            'imageUrl': combined_image_path,
            'imageInfo': {
                'background': image_names.get('Layer1', ''),
                'body': image_names.get('Body', ''),
                'boost': image_names.get('Layer3', ''),
                'mouth': image_names.get('Layer4', ''),
                'eyes': image_names.get('Layer5', ''),
                'face': image_names.get('Layer6', ''),
                'holdings': bun_pb_holdings,
                'atk': total_stats['ATK'],
                'def': total_stats['DEF'],
                'speed': total_stats['SPEED'],
                'hp': total_stats['HP'],
                'effect': effect_text,
                'fightCode': fight_code
    }
        })
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Get the PORT from environment variable (Heroku sets this)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)