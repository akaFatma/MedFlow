import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sign-out-button',
  template: `
    <button
      class="absolute top-4 right-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
      (click)="signOut()"
    >
      Sign Out
    </button>
  `,
  styles: [],
})
export class SignOutButtonComponent {
  constructor(private router: Router) {}

  signOut(): void {
    this.router.navigate(['/login']);
  }
}
