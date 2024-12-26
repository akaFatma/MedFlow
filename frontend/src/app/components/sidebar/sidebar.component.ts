import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface MenuItem {
  icon: string;
  label: string;
  isPrimary?: boolean;
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  template: `
    <aside
      class="h-[98vh] w-[18vw] bg-white-800 text-[#2B2929] flex flex-col p-4 rounded-[30px] border-[#EAEBF0] border-2 ml-3 mt-3 shadow-[4px_4px_8px_0px_rgba(169,169,169,0.2)]"
    >
      <div class="mb-6">
        <img src="./logo.svg" alt="MedFlow" class="max-w-[150px] mx-auto" />
      </div>

      <nav class="flex-grow flex flex-col space-y-4">
        <button
          *ngFor="let item of menuItems"
          [class]="getButtonClasses(item.isPrimary)"
          (click)="handleMenuClick(item)"
        >
          <img
            [src]="'./' + item.icon"
            [alt]="item.label"
            class="w-5 h-5 mr-3"
          />
          <span class="text-sm font-small">{{ item.label }}</span>
        </button>
      </nav>
    </aside>
  `,
})
export class SidebarComponent {
  menuItems: MenuItem[] = [
    {
      icon: 'add.svg',
      label: 'Gestion des comptes',
      isPrimary: false,
    },
    {
      icon: 'manage.svg',
      label: 'Ajouter dossier',
      isPrimary: true,
    },
  ];

  getButtonClasses(isPrimary: boolean = false): string {
    const baseClasses =
      'flex items-center p-2 w-full text-left rounded-[16px] transition duration-200';

    if (isPrimary) {
      return `${baseClasses} bg-[#027CC0] text-white hover:bg-blue-600`;
    }

    return `${baseClasses} bg-white-700 hover:bg-gray-100`;
  }

  handleMenuClick(item: MenuItem): void {
    console.log('Menu item clicked:', item.label);
  }
}
