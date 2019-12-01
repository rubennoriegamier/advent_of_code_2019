import fileinput


def main():
    module_masses = list(map(int, fileinput.input()))
    print(total_fuel_required(module_masses))
    print(total_fuel_required_with_fuel_as_module(module_masses))


def fuel_required(module_mass):
    return module_mass // 3 - 2


def total_fuel_required(module_masses):
    return sum(map(fuel_required, module_masses))


def fuel_required_with_fuel_as_module(module_mass):
    fuel_mass = max(0, fuel_required(module_mass))

    # 9 // 3 - 2 == 1
    # 8 // 3 - 2 == 0
    return fuel_mass if fuel_mass <= 8 else fuel_mass + fuel_required_with_fuel_as_module(fuel_mass)


def total_fuel_required_with_fuel_as_module(module_masses):
    return sum(map(fuel_required_with_fuel_as_module, module_masses))


if __name__ == '__main__':
    main()
