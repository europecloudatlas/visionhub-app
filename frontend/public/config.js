// This file will be ignored when building docker image, instead I will populate config file using configmap.yaml in helm
window.ENV = {
    API_URL: 'https://visionhub-api-dev.europecloudatlas.com',
    ENVIRONMENT: 'dev',
    VERSION: 'latest'
};