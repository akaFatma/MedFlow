export interface Patient {
    nom: string;
    prenom: string;
    nss: number;
    etat: 'ouvert' | 'fermé';
  }