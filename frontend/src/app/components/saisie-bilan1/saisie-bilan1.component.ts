import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-saisie-bilan1',
  templateUrl: './saisie-bilan1.component.html',
  styleUrls: ['./saisie-bilan1.component.scss'],
})
export class SaisieBilan1Component implements OnInit {
  bilanId: string | null = null;

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    // Subscribe to query parameters to retrieve the 'id'
    this.route.queryParams.subscribe((params) => {
      this.bilanId = params['id'];  // Retrieves the modified 'id' from the URL
    });
  }
}
