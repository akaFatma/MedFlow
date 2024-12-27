import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> | Promise<boolean> | boolean {
    if (!this.authService.isAuthentificated()) {
      this.router.navigate(['/login']);
      return false;
    }

    const expectedRole = route.data['role'];
    const userRole = this.authService.getUserRole();
    
    console.log('Expected role:', expectedRole);
    console.log('User role:', userRole);
    
    // Normalize both roles for comparison
    if (this.normalizeRole(userRole) === this.normalizeRole(expectedRole)) {
      return true;
    } else {
      console.log('Role mismatch - redirecting to unauthorized');
      this.router.navigate(['/unauthorized']);
      return false;
    }
  }

  private normalizeRole(role: string): string {
    return role.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }
}
