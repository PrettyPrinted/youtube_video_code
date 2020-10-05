doctors = ['Dr. Leonard McCoy', 'Dr. Beverly Crusher', 'Dr. Julian Bashir', 'The Doctor', 'Dr. Phlox']

names = []

#for doctor in doctors:
    #if doctor.startswith('Dr. '):
    #    names.append(doctor[4:])
    #else:
    #    names.append(doctor)
#    names.append(doctor.removeprefix('Dr. '))

names = [doctor.removeprefix('Dr. ') for doctor in doctors]
print(names)