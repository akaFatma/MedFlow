import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { SaisieBilanService } from '../../services/saisie-bilan.service';

@Component({
  selector: 'app-saisie-bilan-radio',
  templateUrl: './saisie-bilan-radio.component.html',
  styleUrls: ['./saisie-bilan-radio.component.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule],
})
export class SaisieBilanRadioComponent implements OnInit {
  bilanId: any; // ID du bilan
  prescription: any; // Données de la prescription
  compteRendu = ''; // Texte du compte rendu
  selectedFile: File | null = null; // Fichier sélectionné
  selectedFileName: string = "Aucun fichier n'a été sélectionné"; // Nom du fichier sélectionné

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private saisieBilanService: SaisieBilanService
  ) {}

  ngOnInit(): void {
    // Récupération de l'ID depuis les paramètres de la route
    this.route.queryParams.subscribe((params) => {
      this.bilanId = params['id'];
      console.log('Bilan ID:', this.bilanId);
    });

    // Chargement des données de la prescription
    if (this.bilanId) {
      this.loadPrescription(this.bilanId);
    } else {
      console.error('Bilan ID non trouvé dans les paramètres de la route.');
    }
  }

  // Chargement de la prescription depuis le backend
  loadPrescription(id: number): void {
    this.saisieBilanService.getPrescriptionRadio(id).subscribe({
      next: (response) => {
        console.log('Prescription data:', response);
        this.prescription = response;
      },
      error: (error) => {
        console.error('Error loading prescription:', error);
      },
    });
  }

  // Gestion de la sélection de fichier
  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      this.selectedFileName = this.selectedFile.name;
      console.log('Fichier sélectionné :', this.selectedFileName);
    } else {
      this.selectedFile = null;
      this.selectedFileName = "Aucun fichier n'a été sélectionné";
    }
  }

  // Envoi du compte rendu et de l'image au backend
  sendToBackend(): void {
    if (!this.selectedFile) {
      console.error('Aucun fichier sélectionné.');
      alert('Veuillez sélectionner une image avant de soumettre.');
      return;
    }

    if (!this.compteRendu || this.compteRendu.trim() === '') {
      console.error('Le compte rendu est vide.');
      alert('Veuillez entrer un compte rendu avant de confirmer.');
      return;
    }

    const formData = new FormData();
    formData.append('image', this.selectedFile, this.selectedFile.name); // Ajouter le fichier image
    formData.append('compteRendu', this.compteRendu); // Ajouter le texte du compte rendu

    // Appel au service pour envoyer les données
    this.saisieBilanService.postCompteRendu(this.bilanId, formData).subscribe({
      next: (response) => {
        console.log('Compte rendu et image envoyés avec succès :', response);
        alert('Les données ont été envoyées avec succès.');

      },
      error: (error) => {
        console.error('Erreur lors de l\'envoi des données :', error);
        alert(
          'Une erreur est survenue lors de l\'envoi des données. Veuillez réessayer.'
        );
      },
    });
  }
}
