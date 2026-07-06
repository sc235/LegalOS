import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

interface Lead {
  name: string;
  cabinet: string;
  email: string;
  phone: string;
  country: string;
}

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './landing.component.html',
  styleUrl: './landing.component.css'
})
export class LandingComponent {
  lead: Lead = {
    name: '',
    cabinet: '',
    email: '',
    phone: '',
    country: 'Sénégal'
  };

  isSubmitting = false;
  formSubmitted = false;

  onSubmit(event: Event) {
    event.preventDefault();
    if (!this.lead.name || !this.lead.email || !this.lead.phone) return;

    this.isSubmitting = true;

    // Simulation de l'envoi de lead marketing
    setTimeout(() => {
      this.isSubmitting = false;
      this.formSubmitted = true;
    }, 1200);
  }

  resetForm() {
    this.lead = {
      name: '',
      cabinet: '',
      email: '',
      phone: '',
      country: 'Sénégal'
    };
    this.formSubmitted = false;
  }
}
