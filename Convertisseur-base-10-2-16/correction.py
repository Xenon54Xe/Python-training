import math
import tkinter as tk

"""
Variables globales (ce n'est pas nécéssaire de toutes les regrouper au même 
endroit mais c'est plus propre)
"""
_ref = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "A",
        11: "B",
        12: "C",
        13: "D",
        14: "E",
        15: "F",
        # la suite est utile uniquement pour la question bonus *****IV*****
        16: "G",
        17: "H",
        18: "I",
        19: "J",
        20: "K",
        21: "L",
        22: "M",
        23: "N",
        24: "O",
        25: "P",
        26: "Q",
        27: "R",
        28: "S",
        29: "T",
        30: "U",
        31: "V",
        32: "W",
        33: "X",
        34: "Y",
        35: "Z"
    }
_current_mode = "decimal"
_decimal_m = "decimal"
_binary_m = "binary"
_hexadecimal_m = "hexadecimal"


"""
Définition des fonction permettant le fonctionnement du script *****I et II*****
"""


def detect_base(number: str):  # Etape : *****I-2 et I-3.A*****
    global _decimal_m, _binary_m, _hexadecimal_m, _ref

    possible_value = [_ref[i] for i in _ref.keys()]
    decimal = True
    binary = True
    hexadecimal = True

    for i in number:
        if i not in ["0", "1"]:
            binary = False

        try:
            int(i)
        except:
            decimal = False

        if i not in possible_value:
            hexadecimal = False

    if not (binary or decimal or hexadecimal):
        return None
    elif binary:
        return _binary_m
    elif decimal:
        return _decimal_m
    else:
        return _hexadecimal_m


def dec_to_bin(number: str) -> str:  # *****II-1*****
    if number == "0":
        return "0"

    number = int(number)
    nb_bin = ""
    while number > 0:
        nb_bin = f"{number % 2}{nb_bin}"
        number //= 2
    return nb_bin


def bin_to_dec(number: str):  # *****II-2*****
    power = len(number) - 1
    value = 0
    for i in range(len(number)):
        value += int(number[i]) * int(math.pow(2, power - i))
    return str(value)


def bin_to_hex(number: str):  # *****II-3*****
    global _ref

    num = number
    bin_list = []
    to_remove = len(num) % 4
    if to_remove != 0:
        bin_list.append(num[:to_remove])
    num = num[to_remove:]

    while len(num) > 0:
        bin_list.append(num[:4])
        num = num[4:]

    result = ""
    for i in bin_list:
        decimal = bin_to_dec(i)
        hexadecimal = _ref[int(decimal)]
        result += hexadecimal
    return result


def invert_dictionary(dictionary: dict):
    """
    Attention, cette fonction peut ne pas fonctionner si le dictionnaire associe plusieurs fois la
    même valeur à différentes clés
    :param dictionary:
    :return:
    """
    """
    J'avais la flemme de recopier le dictionnaire 'ref' ducoup j'ai fais une 
    fonction pour le faire à ma place. Cette fonction permet d'intervertir 
    les clés et les objets du dictionnaire. (les clés deviennent les objets et
    inversement)
    """
    new_dict = {}
    for key in dictionary.keys():
        value = dictionary[key]
        new_dict[value] = key
    return new_dict


def hex_to_dec(number):  # *****II-4*****
    global _ref

    new_ref = invert_dictionary(_ref)
    power = len(number) - 1
    value = 0
    for i in range(len(number)):
        num = new_ref[number[i]]
        value += num * int(math.pow(16, power - i))
    return str(value)


def convert(n: int, m: int, number: str) -> str:  # *****IV*****
    """
    Attention, cette fonction peut ne pas fonctionner si le nombre à convertir
    ne peut pas être interprété dans la base n
    :param n:
    :param m:
    :param number:
    :return:
    """
    global _ref
    inverted_ref = invert_dictionary(_ref)

    # on définit la base la plus petite comme étant la base 2 et la plus grande
    # la base 35
    if not 2 <= n <= 35 or not 2 <= m <= 35 or n == m:
        raise Exception("Les bases renseignées doivent être comprises entre 2 et 35 et ne doivent pas être égales")

    """
    Partie permettant de vérifier que le nombre est interprétable dans la base n
    """
    keys = []
    for i in inverted_ref.keys():
        keys.append(i)

    for i in number:
        if i not in keys[:n]:
            raise Exception(f"Le nombre renseigné {number} n'est pas interprétable dans la base {n}")

    """
    Première étape: convertir le nombre de la base n vers la base 10
    """
    power = len(number) - 1
    value = 0
    for i in range(len(number)):
        num = inverted_ref[number[i]]
        value += num * math.pow(n, power - i)

    """
    Deuxième étape: convertir le nombre de la base 10 vers la base m
    """
    result = ""
    while value > 0:
        rest = value % m
        result = _ref[rest] + result
        value //= m

    return result


def base(user_base, detected_base):  # *****I-3.C*****
    global _binary_m, _decimal_m, _hexadecimal_m

    if user_base == _binary_m and detected_base == _binary_m:
        return _binary_m
    elif user_base == _decimal_m and detected_base in [_binary_m, _decimal_m]:
        return _decimal_m
    return _hexadecimal_m


def main(*args):  # *****III-1*****
    """
    Fonction appelée à chaque fois que le nombre ou le mode est modifié,
    elle englobe à elle seule presque toute l'étape III
    :param args:
    :return:
    """
    global _current_mode

    number_to_convert = select_number_vr.get()  # *****III-2.A*****
    if number_to_convert == "":
        number_to_convert = "0"

    number_base = detect_base(number_to_convert)  # *****III-2.B et III-2.C*****
    if number_base is None:
        raise Exception("Le nombre n'est pas conforme")

    selected_base = base(_current_mode, number_base)  # *****III-2.C*****

    """
    La structure en if, elif, else suivante représente l'étape *****III-2.D*****
    """
    if selected_base == _binary_m:
        select_number_type_vw.set("Type détecté: binaire")

        number_dec = bin_to_dec(number_to_convert)  # *****III-2.D*****
        number_hex = bin_to_hex(number_to_convert)  # *****III-2.D*****

        result_one_vw.set(number_dec)  # *****III-2.E*****
        result_two_vw.set(number_hex)  # *****III-2.E*****

        result_one_label_vw.set("Décimal:")
        result_two_label_vw.set("Hexadécimal:")
    elif selected_base == _decimal_m:
        select_number_type_vw.set("Type détecté: décimal")

        number_bin = dec_to_bin(number_to_convert)  # *****III-2.D*****
        number_hex = bin_to_hex(number_bin)  # *****III-2.D*****

        result_one_vw.set(number_bin)  # *****III-2.E*****
        result_two_vw.set(number_hex)  # *****III-2.E*****

        result_one_label_vw.set("Binaire:")
        result_two_label_vw.set("Hexadécimal:")
    else:
        select_number_type_vw.set("Type détecté: hexadécimal")

        number_dec = hex_to_dec(number_to_convert)  # *****III-2.D*****
        number_bin = dec_to_bin(number_dec)  # *****III-2.D*****

        result_one_vw.set(number_bin)  # *****III-2.E*****
        result_two_vw.set(number_dec)  # *****III-2.E*****

        result_one_label_vw.set("Binaire:")
        result_two_label_vw.set("Décimal:")

    """
    Ajout de la partie bonus *****IV*****
    """
    number_to_convert_bonus = number_bonus_vr.get()
    if number_to_convert_bonus == "":
        number_to_convert_bonus = "0"

    base_n = base_n_vr.get()
    base_m = base_m_vr.get()
    if base_n == "" or base_m == "":
        return

    try:
        base_n = int(base_n_vr.get())
        base_m = int(base_m_vr.get())
    except:
        raise Exception("Partie bonus: les bases renseignées ne sont pas des nombres !")

    try:
        converted_number = convert(base_n, base_m, number_to_convert_bonus)
        result_bonus_vw.set(converted_number)
    except Exception:
        raise


"""
Partie permettant la récupération du nombre à convertir et 
l'affichage du résultat grâce à tkinter
"""
# Création de la fênetre avec tkinter
window = tk.Tk()
window.geometry("560x200")
window.minsize(560, 200)
window.title("Hexadecimator")

"""
La partie DM sera dans la frame_main
"""

frame_main = tk.Frame(window, relief="groove", borderwidth=1)

"""
Récupération du nombre à convertir avec tkinter
"""
# Label affiché au-dessus du nombre à écrire (label = texte)
select_number_label = tk.Label(frame_main, text="Nombre à convertir\n"
                                                "S'il est hexadécimal il faut l'écrire avec "
                                                "des lettres majuscules", fg="blue")
select_number_label.pack()

# Label base du nombre détecté
select_number_type_vw = tk.StringVar()
select_number_type_vw.set("Base détectée:")
select_number_type_label = tk.Label(frame_main, textvariable=select_number_type_vw, fg="green")
select_number_type_label.pack()

"""
*****I-1*****
"""
# Entrée permettant d'écrire le nombre à convertir (entry = zone de saisie de texte)
select_number_vr = tk.StringVar()
select_number_vr.trace("w", main)
select_number_entry = tk.Entry(frame_main, textvariable=select_number_vr)
select_number_entry.pack()

"""
Partie affichage du résultat avec tkinter *****III-2.E*****
"""
# Label résultat
result_label = tk.Label(frame_main, text="Résultats:", fg="blue")
result_label.pack()

# frame pour le résultat
# (frame = boite dans laquelle peuvent être rangés des label, des boutton,...)
# les frames permettent de mieux organiser
result_frame = tk.Frame(frame_main, relief="groove", borderwidth=1)

# label du premier résultat
result_one_label_vw = tk.StringVar()
result_one_label_vw.set("Binaire :")
result_one_label = tk.Label(result_frame, textvariable=result_one_label_vw)
result_one_label.grid(column=0, row=1)
# entrée du premier résultat *****III-2.E*****
result_one_vw = tk.StringVar()
result_one_entry = tk.Entry(result_frame, textvariable=result_one_vw)
result_one_entry.grid(column=1, row=1)

# label du deuxième résultat
result_two_label_vw = tk.StringVar()
result_two_label_vw.set("Hexadécimal :")
result_two_label = tk.Label(result_frame, textvariable=result_two_label_vw)
result_two_label.grid(column=0, row=2)
# entrée du deuxième résultat *****III-2.E*****
result_two_vw = tk.StringVar()
result_two_entry = tk.Entry(result_frame, textvariable=result_two_vw)
result_two_entry.grid(column=1, row=2)

result_frame.pack()

"""
Sélection du mode, ici l'utilisateur dit quelle base est 
associée au nombre à convertir *****I-3.B*****
"""
# label au-dessus de la sélection du mode
select_mode_vw = tk.StringVar()
select_mode_vw.set("Mode: Décimal")
select_mode_label = tk.Label(frame_main, textvariable=select_mode_vw, fg="green")
select_mode_label.pack()


def toggle_current_mode():
    """
    Fonction permettant de changer le texte de select_mode_label
    """
    global _current_mode

    if _current_mode == _decimal_m:
        _current_mode = _binary_m
        select_mode_vw.set("Mode : Binaire")
    elif _current_mode == _binary_m:
        _current_mode = _hexadecimal_m
        select_mode_vw.set("Mode : Hexadécimal")
    else:
        _current_mode = _decimal_m
        select_mode_vw.set("Mode : Décimal")
    main()


# Boutton permettant de changer le mode *****III-3.B*****
select_mode_button = tk.Button(frame_main, text="Changer le mode", fg="red", command=toggle_current_mode)
select_mode_button.pack()

"""
Ajout de la partie bonus dans l'affichage tkinter *****IV*****
"""

bonus_frame = tk.Frame(window, relief="groove", borderwidth=1)

# label bonus
bonus_label = tk.Label(bonus_frame, text="Partie bonus", fg="red")
bonus_label.pack()

# label nombre à convertir
number_bonus_label = tk.Label(bonus_frame, text="Nombre à convertir", fg="blue")
number_bonus_label.pack()

# entrée du nombre à convertir
number_bonus_vr = tk.StringVar()
number_bonus_vr.trace("w", main)
number_bonus_entry = tk.Entry(bonus_frame, textvariable=number_bonus_vr)
number_bonus_entry.pack()

# frame bases
bases_frame = tk.Frame(bonus_frame, relief="groove", borderwidth=1)

# label bonus
base_n_label = tk.Label(bases_frame, text="Base du nombre :", fg="green")
base_n_label.grid(column=0, row=0)

# entrée base n du bonus
base_n_vr = tk.StringVar()
base_n_vr.set("2")
base_n_vr.trace("w", main)
base_n_entry = tk.Entry(bases_frame, textvariable=base_n_vr)
base_n_entry.grid(column=1, row=0)

# label bonus
base_m_label = tk.Label(bases_frame, text="Base cible :", fg="green")
base_m_label.grid(column=0, row=1)

# entrée base m du bonus
base_m_vr = tk.StringVar()
base_m_vr.set("10")
base_m_vr.trace("w", main)
base_m_entry = tk.Entry(bases_frame, textvariable=base_m_vr)
base_m_entry.grid(column=1, row=1)

bases_frame.pack()

# label résultat
result_bonus_label = tk.Label(bonus_frame, text="Résultat", fg="blue")
result_bonus_label.pack()

# entrée résultat du bonus
result_bonus_vw = tk.StringVar()
result_bonus_entry = tk.Entry(bonus_frame, textvariable=result_bonus_vw)
result_bonus_entry.pack()

"""
Finalisation
"""
main()  # appel de la fonction main

frame_main.grid(column=0, row=0, sticky="n")
bonus_frame.grid(column=1, row=0, sticky="n")

window.mainloop()  # pour que la fênetre de tkinter s'affiche il faut écrire cette ligne
