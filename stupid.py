import os
import csv
amplitudes = []
v_m = []
t_m = []
with  open('syn_stim.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        ampl = float(row[0])
        amplitudes.append(ampl)

print(amplitudes)
"""
def make_text(a,name):
    i=0
    b= {"a1_0": 432.30906917672496,"a1_1": 0.36509351199795115,"b1_0": 0.25092446546577984,"b1_1": 0.10368038143975336,"a2_0": 32.29917113475886,"a2_1": 0.32872066979489867,"b2_0": 416.3686624500136,"b2_1": 0.6047490120163639,"a3_0": 439.61106954943006,"a3_1": 0.15606269154605926,"b3_0": 4427.707117069347,"b3_1": 0.07861524367591624,"bh_0": 2.7863087984099355,"bh_1": 2.541390054437568,"bh_2": 0.08415464651758393,"ah_0": 2.9933106051320424,"ah_1": 4381.42483380878,"ah_2": 0.05434382499259825,"vShift": -8.00133802374923,"vShift_inact": 9.116289162920513,"maxrate": 30.716532389329487}
    for x, y in b.items():
        b[x] = a[i]
        i+=1
    
    text_file_name = f"na12_R850P_{name}.txt"
    text_file_path = os.path.join('params', text_file_name)
    with open(text_file_path, "w") as text_file:
        text_file.write(f"{b}")
"""