import matplotlib.pyplot as plt
from matplotlib import style                # --- Для красивого оформления графиков
from prettytable import PrettyTable         # --- Для оформления вывода в виде таблички

style.use('ggplot')

constants = {'a1': 15.7,
             'a2': 17.8,
             'a3': 0.71,
             'a4': 23.7,
             'a5': 34.0,
             'r0': 1.4,
             'delta_MH': 7.289,
             'delta_mn': 8.071}

elements = {'H': 1, 'He': 2, 'Li':3, 'Be':4, 'B':5, 'C':6,
            'N':7, 'O':8, 'F':9, 'Ne':10, 'Na': 11, 'Mg': 12,
            'Al': 13, 'Si':14, 'P':15, 'S':16, 'Cl':17, 'Ar':18,
            'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22, 'V':23, 'Cr':24,
            'Mn':25, 'Fe':26, 'Co':27, 'Ni':28, 'Cu':29, 'Zn':30, 'Ga':31, 'Ge':32,
            'U':92, }


class Element:
    def __init__(self, name: str, massNumber: int, atomicNumber: int):
        self.name = name
        self.A = massNumber
        self.Z = atomicNumber

    def getEnergy(self, N: int = 3) -> float:
        '''
        Функция вычисляет значение энергии связи атома
        :param: N: Type is Integer. Число знаков, до которого нужно округлить число
        :return: Type is float. Значение энергии в МэВ
        '''
        A,Z = self.A, self.Z
        G = A*constants.get('a1')-(A**(2/3))*constants.get('a2')-constants.get('a3')*Z*(Z-1)/(A**(1/3))-constants.get('a4')*((A-2*Z)**2)/A
        if A%2 == 0 and Z%2 == 0: G += constants.get('a5')*A**(-3/4)
        elif A%2 != 0 and Z%2 != 0: G -= constants.get('a5') * A ** (-3 / 4)
        return round(G,N)

    def getSpecificEnergy(self, N: int = 3) -> float:
        '''
        Функция вычисляет значение энергии связи атома
        :param: N: Type is Integer. Число знаков, до которого нужно округлить число
        :return: Type is float. Значение удельной энергии в МэВ
        '''
        A, Z = self.A, self.Z
        SG = self.getEnergy()/A
        return round(SG,N)

    def getAtomicMass(self, N: int = 3) -> float:
        G = self.getEnergy()
        A, Z = self.A, self.Z
        delta_M = Z * constants.get('delta_MH') + (A-Z) * constants.get('delta_mn') - G
        M = delta_M + A * 931.5
        return round(M/931.5, N)


    def getNuclearRadius(self, N: int = 2) -> float:
        '''
        Функция вычисляет радиус ядра атома
        :param: N: Type is Integer. Число знаков, до которого нужно округлить число
        :return: Type is float. Значение радиуса в Фм
        '''
        A = self.A
        radius = constants.get('r0')*(A**(1/3))
        return round(radius, N)

    def checkResistanceToAlphaDecay(self):
        '''
        Функция проверяет устойчивость атома к альфа-распаду
        '''
        Z = self.Z
        if Z > 82 or Z == 62 or Z == 78:
            return "Подвержен альфа-распаду"
        else:
            return "Устойчив к альфа-распаду"

    def checkResistanceToBetaDecay(self):
        '''
        Функция проверяет устойчивость атома к бета-распаду
        '''
        Z = self.Z
        A = self.A
        if Z == A-Z:
            return "Устойчив к бета-распаду"
        else: return "Подвержен бета-распаду"


    def checkAbilityToSplitOnTwoParticles(self):
        '''
        Функция проверяет возможность деления данного изотопа на 2 одинаковых четно-четных осколка.
        '''
        A, Z = self.A, self.Z
        if A % 4 and Z % 4:
            return "Деление ядра на 2 четно-четных осколка возможно"
        else: return "Деление ядра на 2 четно-четных осколка невозможно"

arElems = []

print(elements.keys())
print('Чтобы закончить, нажмите Enter')
while True:
    el = str(input("Введите название элемента в соответствии с таблицей Менделеева через тире с массовым числом, пример U-238"))
    if el != '':
        list_el = el.split('-')
        a = int(list_el[1])
        name = list_el[0]
        print(name, a)
        element = Element(name, a, elements.get(name))
        arElems.append(element)
    else: break


table = PrettyTable(['Name', 'Specific Energy', 'Atomic mass', 'Nuclear radius', 'Resistance to alpha-decay', 'ability to split on 2 part-s.', 'Resistance to beta-decay'])
for i in arElems:
    table.add_row([f'{i.name}', f'{i.getSpecificEnergy()}', f'{i.getAtomicMass()}', f'{i.getNuclearRadius()}', f'{i.checkResistanceToAlphaDecay()}', f'{i.checkAbilityToSplitOnTwoParticles()}', f'{i.checkResistanceToBetaDecay()}'])

print(table)


ax = plt.subplot (2, 1, 1)
for i in arElems:
    plt.scatter(i.Z, i.getNuclearRadius(), label=f'{i.name}')

ax.set_xlabel('Зарядовое число Z')
ax.set_ylabel('Радиус, Фм')
plt.grid(True, color='#DDDDDD', linestyle='--', which='both')
ax.set_title('Зависимость радиуса ядра R от зарядового числа Z')
plt.legend()


bx = plt.subplot (2, 1, 2)
for i in arElems:
    plt.scatter(i.Z, i.getSpecificEnergy(), label=f'{i.name}')

plt.grid(True, color='#DDDDDD', linestyle='--', which='both')
bx.set_xlabel('Зарядовое число Z')
bx.set_ylabel('Удельная энергия, МэВ')
bx.set_title('Зависимость радиуса ядра R от зарядового числа Z')
plt.legend()
plt.show()

