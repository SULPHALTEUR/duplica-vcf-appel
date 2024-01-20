# il faut installer python et aussi vobject 
#pip install vobject

import vobject

# Définir le chemin du fichier d'entrée et de sortie
input_file = "contacts.vcf"
output_file = "contacts_sans_duplication.vcf"

# Créer un dictionnaire pour stocker les contacts basés sur le champ "N" (nom) ou l'adresse e-mail
contacts = {}

# Lire le fichier VCF et traiter les contacts
with open(input_file, "r", encoding="utf-8") as vcf_file:
    components = vobject.readComponents(vcf_file)
    
    for component in components:
        # Obtenez la valeur du champ "N" (nom) du contact
        n_value = component.n.value if hasattr(component, 'n') else ''
        
        # Obtenez la valeur du champ "EMAIL" (adresse e-mail) du contact
        email_value = component.email.value if hasattr(component, 'email') else ''
        
        # Si le champ "N" est vide, utilisez le champ "EMAIL" pour le nom
        if not n_value and email_value:
            n_value = email_value
        
        # Supprimez les espaces et les caractères vides du champ "N" pour éviter les faux doublons
        n_value_cleaned = "".join(str(n_value).split())
        
        # Si le champ "N" est déjà dans le dictionnaire, ignorez ce contact (doublon)
        if n_value_cleaned in contacts:
            continue
        
        # Ajoutez le contact au dictionnaire
        contacts[n_value_cleaned] = component

# Écrivez les contacts dans le fichier de sortie en générant le fichier manuellement
with open(output_file, "w", encoding="utf-8") as output_vcf:
    for contact in contacts.values():
        output_vcf.write("BEGIN:VCARD\n")
        output_vcf.write("VERSION:3.0\n")
        
        if hasattr(contact, 'n'):
            output_vcf.write(f"N:{contact.n.value}\n")
        
        # Ajoutez la ligne FN en utilisant le champ "N" comme nom
        if hasattr(contact, 'n'):
            output_vcf.write(f"FN:{contact.n.value}\n")
        
        # Copiez le champ REV du contact d'origine
        if hasattr(contact, 'rev'):
            output_vcf.write(f"REV:{contact.rev.value}\n")
        
        # Ajoutez le champ EMAIL manuellement
        if hasattr(contact, 'email'):
            email_values = contact.email.value.split(',')
            for email in email_values:
                output_vcf.write(f"EMAIL;type=INTERNET;type=HOME;type=pref:{email.strip()}\n")
        
        output_vcf.write("END:VCARD\n")

print(f"Contacts dupliqués supprimés, {len(contacts)} contacts uniques sauvegardés dans '{output_file}'.")
