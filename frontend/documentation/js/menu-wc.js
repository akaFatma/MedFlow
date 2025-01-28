'use strict';

customElements.define('compodoc-menu', class extends HTMLElement {
    constructor() {
        super();
        this.isNormalMode = this.getAttribute('mode') === 'normal';
    }

    connectedCallback() {
        this.render(this.isNormalMode);
    }

    render(isNormalMode) {
        let tp = lithtml.html(`
        <nav>
            <ul class="list">
                <li class="title">
                    <a href="index.html" data-type="index-link">gestion-dpi documentation</a>
                </li>

                <li class="divider"></li>
                ${ isNormalMode ? `<div id="book-search-input" role="search"><input type="text" placeholder="Type to search"></div>` : '' }
                <li class="chapter">
                    <a data-type="chapter-link" href="index.html"><span class="icon ion-ios-home"></span>Getting started</a>
                    <ul class="links">
                        <li class="link">
                            <a href="overview.html" data-type="chapter-link">
                                <span class="icon ion-ios-keypad"></span>Overview
                            </a>
                        </li>
                        <li class="link">
                            <a href="index.html" data-type="chapter-link">
                                <span class="icon ion-ios-paper"></span>README
                            </a>
                        </li>
                                <li class="link">
                                    <a href="dependencies.html" data-type="chapter-link">
                                        <span class="icon ion-ios-list"></span>Dependencies
                                    </a>
                                </li>
                                <li class="link">
                                    <a href="properties.html" data-type="chapter-link">
                                        <span class="icon ion-ios-apps"></span>Properties
                                    </a>
                                </li>
                    </ul>
                </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#components-links"' :
                            'data-bs-target="#xs-components-links"' }>
                            <span class="icon ion-md-cog"></span>
                            <span>Components</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="components-links"' : 'id="xs-components-links"' }>
                            <li class="link">
                                <a href="components/AddDPIComponent.html" data-type="entity-link" >AddDPIComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/AppComponent.html" data-type="entity-link" >AppComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/BienvenuComponentComponent.html" data-type="entity-link" >BienvenuComponentComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/BilanComponent.html" data-type="entity-link" >BilanComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/ConsulterDPIPovPatientComponent.html" data-type="entity-link" >ConsulterDPIPovPatientComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/ConsultPatientComponent.html" data-type="entity-link" >ConsultPatientComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/HeaderComponent.html" data-type="entity-link" >HeaderComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/HomePageComponent.html" data-type="entity-link" >HomePageComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/InfermierLandingPageComponent.html" data-type="entity-link" >InfermierLandingPageComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/InfermierTableComponent.html" data-type="entity-link" >InfermierTableComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/LaborantinComponent.html" data-type="entity-link" >LaborantinComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/LaboTableComponent.html" data-type="entity-link" >LaboTableComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/LoginComponent.html" data-type="entity-link" >LoginComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/LoginPageComponent.html" data-type="entity-link" >LoginPageComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/MedecinLandingPageComponent.html" data-type="entity-link" >MedecinLandingPageComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/MedecinTableComponent.html" data-type="entity-link" >MedecinTableComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/MedicalHistoryComponent.html" data-type="entity-link" >MedicalHistoryComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/NouvelleConsultationComponent.html" data-type="entity-link" >NouvelleConsultationComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/OrdonnanceComponent.html" data-type="entity-link" >OrdonnanceComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/PersonalInfoCardComponent.html" data-type="entity-link" >PersonalInfoCardComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/QrScannerComponent.html" data-type="entity-link" >QrScannerComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/RadiologueComponent.html" data-type="entity-link" >RadiologueComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/RadioTableComponent.html" data-type="entity-link" >RadioTableComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/ResumeComponent.html" data-type="entity-link" >ResumeComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/SaisieBilanComponent.html" data-type="entity-link" >SaisieBilanComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/SaisieBilanRadioComponent.html" data-type="entity-link" >SaisieBilanRadioComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/SearchBarComponent.html" data-type="entity-link" >SearchBarComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/SideBarComponent.html" data-type="entity-link" >SideBarComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/SidebarComponent.html" data-type="entity-link" >SidebarComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/SignOutButtonComponent.html" data-type="entity-link" >SignOutButtonComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/SoinsComponent.html" data-type="entity-link" >SoinsComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/SoinsHistoryComponent.html" data-type="entity-link" >SoinsHistoryComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/SuccessNotifComponent.html" data-type="entity-link" >SuccessNotifComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/UnauthorizedComponent.html" data-type="entity-link" >UnauthorizedComponent</a>
                            </li>
                            <li class="link">
                                <a href="components/UnauthorizedPageComponent.html" data-type="entity-link" >UnauthorizedPageComponent</a>
                            </li>
                        </ul>
                    </li>
                        <li class="chapter">
                            <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#injectables-links"' :
                                'data-bs-target="#xs-injectables-links"' }>
                                <span class="icon ion-md-arrow-round-down"></span>
                                <span>Injectables</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                            <ul class="links collapse " ${ isNormalMode ? 'id="injectables-links"' : 'id="xs-injectables-links"' }>
                                <li class="link">
                                    <a href="injectables/AuthService.html" data-type="entity-link" >AuthService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/ConsultationHistoryService.html" data-type="entity-link" >ConsultationHistoryService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/ConsultationPatientService.html" data-type="entity-link" >ConsultationPatientService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/ConsultationService.html" data-type="entity-link" >ConsultationService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/InfermierService.html" data-type="entity-link" >InfermierService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/LaborantinService.html" data-type="entity-link" >LaborantinService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/MedecinService.html" data-type="entity-link" >MedecinService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/PatientService.html" data-type="entity-link" >PatientService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/RadiologueService.html" data-type="entity-link" >RadiologueService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/SaisieBilanService.html" data-type="entity-link" >SaisieBilanService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/SearchService.html" data-type="entity-link" >SearchService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/SoinHistoryService.html" data-type="entity-link" >SoinHistoryService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/UserInfoService.html" data-type="entity-link" >UserInfoService</a>
                                </li>
                            </ul>
                        </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#interceptors-links"' :
                            'data-bs-target="#xs-interceptors-links"' }>
                            <span class="icon ion-ios-swap"></span>
                            <span>Interceptors</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="interceptors-links"' : 'id="xs-interceptors-links"' }>
                            <li class="link">
                                <a href="interceptors/AuthInterceptor.html" data-type="entity-link" >AuthInterceptor</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#guards-links"' :
                            'data-bs-target="#xs-guards-links"' }>
                            <span class="icon ion-ios-lock"></span>
                            <span>Guards</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="guards-links"' : 'id="xs-guards-links"' }>
                            <li class="link">
                                <a href="guards/RoleGuard.html" data-type="entity-link" >RoleGuard</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#interfaces-links"' :
                            'data-bs-target="#xs-interfaces-links"' }>
                            <span class="icon ion-md-information-circle-outline"></span>
                            <span>Interfaces</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? ' id="interfaces-links"' : 'id="xs-interfaces-links"' }>
                            <li class="link">
                                <a href="interfaces/Alert.html" data-type="entity-link" >Alert</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Consultation.html" data-type="entity-link" >Consultation</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ConsultationData.html" data-type="entity-link" >ConsultationData</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Patient.html" data-type="entity-link" >Patient</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/patient.html" data-type="entity-link" >patient</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Patient-1.html" data-type="entity-link" >Patient</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/patient-1.html" data-type="entity-link" >patient</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Prescription.html" data-type="entity-link" >Prescription</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/Soins.html" data-type="entity-link" >Soins</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/SoinsData.html" data-type="entity-link" >SoinsData</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/user.html" data-type="entity-link" >user</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#miscellaneous-links"'
                            : 'data-bs-target="#xs-miscellaneous-links"' }>
                            <span class="icon ion-ios-cube"></span>
                            <span>Miscellaneous</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="miscellaneous-links"' : 'id="xs-miscellaneous-links"' }>
                            <li class="link">
                                <a href="miscellaneous/variables.html" data-type="entity-link">Variables</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <a data-type="chapter-link" href="coverage.html"><span class="icon ion-ios-stats"></span>Documentation coverage</a>
                    </li>
                    <li class="divider"></li>
                    <li class="copyright">
                        Documentation generated using <a href="https://compodoc.app/" target="_blank" rel="noopener noreferrer">
                            <img data-src="images/compodoc-vectorise.png" class="img-responsive" data-type="compodoc-logo">
                        </a>
                    </li>
            </ul>
        </nav>
        `);
        this.innerHTML = tp.strings;
    }
});