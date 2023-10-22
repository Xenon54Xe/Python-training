import math
import tkinter as tk

"""
Variables globales (ce n'est pas nécéssaire de toutes les regrouper au même 
endroit mais c'est plus propre)
"""
ref = {
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
        15: "F"
    }
current_mode = "decimal"
_decimal_m = "decimal"
_binary_m = "binary"
_hexadecimal_m = "hexadecimal"


"""
Définition des fonction permettant le fonctionnement du script *****I et II*****
"""


def detect_base(number: str):  # Etape : *****I-2 et I-3.A*****
    global _decimal_m, _binary_m, _hexadecimal_m, ref

    possible_value = [ref[i] for i in ref.keys()]
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
    global ref

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
        hexadecimal = ref[int(decimal)]
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
    global ref

    new_ref = invert_dictionary(ref)
    power = len(number) - 1
    value = 0
    for i in range(len(number)):
        num = new_ref[number[i]]
        value += num * int(math.pow(16, power - i))
    return str(value)


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
    global current_mode

    number_to_convert = select_number_vr.get()  # *****III-2.A*****
    if number_to_convert == "":
        number_to_convert = "0"

    number_base = detect_base(number_to_convert)  # *****III-2.B et III-2.C*****
    if number_base is None:
        raise Exception("Le nombre n'est pas conforme")

    selected_base = base(current_mode, number_base)  # *****III-2.C*****

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
Partie permettant la récupération du nombre à convertir et 
l'affichage du résultat grâce à tkinter
"""
# Création de la fênetre avec tkinter
window = tk.Tk()
window.geometry("360x200")
window.minsize(360, 200)
window.title("Hexadecimator")

"""
Récupération du nombre à convertir avec tkinter
"""
# Label affiché au-dessus du nombre à écrire (label = texte)
select_number_label = tk.Label(window, text="Nombre à convertir\n"
                                            "S'il est hexadécimal il faut l'écrire avec "
                                            "des lettres majuscules", fg="blue")
select_number_label.pack()

# Label base du nombre détecté
select_number_type_vw = tk.StringVar()
select_number_type_vw.set("Base détectée:")
select_number_type_label = tk.Label(window, textvariable=select_number_type_vw, fg="green")
select_number_type_label.pack()

"""
*****I-1*****
"""
# Entrée permettant d'écrire le nombre à convertir (entry = zone de saisie de texte)
select_number_vr = tk.StringVar()
select_number_vr.trace("w", main)
select_number_entry = tk.Entry(window, textvariable=select_number_vr)
select_number_entry.pack()

"""
Partie affichage du résultat avec tkinter *****III-2.E*****
"""
# Label résultat
result_label = tk.Label(window, text="Résultats:", fg="blue")
result_label.pack()

# frame pour le résultat
# (frame = boite dans laquelle peuvent être rangés des label, des boutton,...)
# les frames permettent de mieux organiser
result_frame = tk.Frame(window, relief="groove", borderwidth=1)

# label du premier résultat
result_one_label_vw = tk.StringVar()
result_one_label_vw.set("Binaire:")
result_one_label = tk.Label(result_frame, textvariable=result_one_label_vw)
result_one_label.grid(column=0, row=1)
# entrée du premier résultat *****III-2.E*****
result_one_vw = tk.StringVar()
result_one_entry = tk.Entry(result_frame, textvariable=result_one_vw)
result_one_entry.grid(column=1, row=1)

# label du deuxième résultat
result_two_label_vw = tk.StringVar()
result_two_label_vw.set("Hexadécimal:")
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
select_mode_label = tk.Label(window, textvariable=select_mode_vw, fg="green")
select_mode_label.pack()


def toggle_current_mode():
    """
    Fonction permettant de changer le texte de select_mode_label
    """
    global current_mode

    if current_mode == _decimal_m:
        current_mode = _binary_m
        select_mode_vw.set("Mode : Binaire")
    elif current_mode == _binary_m:
        current_mode = _hexadecimal_m
        select_mode_vw.set("Mode : Hexadécimal")
    else:
        current_mode = _decimal_m
        select_mode_vw.set("Mode : Décimal")
    main()


# Boutton permettant de changer le mode *****III-3.B*****
select_mode_button = tk.Button(window, text="Changer le mode", fg="red", command=toggle_current_mode)
select_mode_button.pack()


"""
Finalisation
"""
main()  # appel de la fonction main

window.mainloop()  # pour que la fênetre de tkinter s'affiche il faut écrire cette ligne
