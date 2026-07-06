import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  email = '';
  password = '';
  errorMessage = '';
  isLoading = false;

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit(event: Event) {
    event.preventDefault();
    if (!this.email || !this.password) return;

    this.isLoading = true;
    this.errorMessage = '';

    // Simulation de connexion pour le prototype
    setTimeout(() => {
      if (this.email.includes('cabinet.com') || this.email.includes('legalos.com') || this.password === 'admin' || this.password.length >= 4) {
        this.authService.setSession(this.email, 'Avocat');
        this.router.navigate(['/dashboard']);
      } else {
        this.errorMessage = 'Identifiants de connexion invalides.';
        this.isLoading = false;
      }
    }, 800);
  }

  loginAs(role: string) {
    this.isLoading = true;
    setTimeout(() => {
      const emailMap: Record<string, string> = {
        avocat: 'associe@cabinet-diallo.com',
        secretaire: 'secretaire@cabinet-diallo.com',
        comptable: 'compta@cabinet-diallo.com'
      };
      this.authService.setSession(emailMap[role] || 'user@cabinet.com', role.toUpperCase());
      this.router.navigate(['/dashboard']);
    }, 500);
  }
}
