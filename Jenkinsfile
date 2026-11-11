pipeline{
  
  agent any
  parameters {
    string(name: 'ENV', defaultValue: 'dev', description: 'Environment to deploy to')
    choice(name: 'ACTION', choices: ['build', 'test', 'deploy'], description: 'Action to perform')
    booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip tests during build')
  }
  stages {
    
    stage ("build") {
      steps {
        echo "building the app"
      }
    }
    
    stage ("test") {
      
      when {
        expression { return !params.SKIP_TESTS }
      }
      steps {
        echo "testing the app"
      }      
    }
    
    stage ("deploy") {
      
      steps {
        echo "deploying the app"
        echo "Deploying to environment: ${params.ENV}"
      }     
    }
  }
}
