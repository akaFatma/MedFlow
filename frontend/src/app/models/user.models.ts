export interface user {
  'patient': {
    'nom': string,
    'prenom': string, 
    'nss': number, 
    'adresse': string, 
    'date_de_naissance': string, 
    'telephone': string, 
    'mutuelle': string, 
    'personne_a_contacter': {
      'nom': string, 
      'prenom': string, 
      'telephone': string
    }, 
  },
  'etat': string
}