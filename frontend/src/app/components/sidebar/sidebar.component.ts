import { Component, HostListener, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faHome, faUserGear, faBars } from '@fortawesome/free-solid-svg-icons';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-sidebar',
  imports: [FontAwesomeModule, CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss'],
})
export class SidebarComponent {
  faHome = faHome; // Icon for Dashboard
  faUserGear = faUserGear; // Icon for Gestion des Patients
  faBars = faBars; // Icon for Hamburger Menu

  isSidebarOpen: boolean = true; // Sidebar visibility
  isMobileView: boolean = false; // Whether the screen size is mobile

  ngOnInit(): void {
    this.checkScreenSize();
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    this.checkScreenSize();
  }

  // Check the screen size and adjust the layout
  private checkScreenSize(): void {
    this.isMobileView = window.innerWidth <= 576;
    if (this.isMobileView) {
      this.isSidebarOpen = false; // Hide sidebar on small screens
    } else {
      this.isSidebarOpen = true; // Show sidebar on larger screens
    }
  }

  // Toggle sidebar visibility
  toggleSidebar(): void {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

  // Navigation logic
  navigateTo(route: string): void {
    console.log(`Navigating to ${route}`);
    // Add actual navigation logic (e.g., Angular Router)
  }
}
