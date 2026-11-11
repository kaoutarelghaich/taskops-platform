pipeline{
  
  agent any
  parameters {
    string(name: 'ENV', defaultValue: 'dev', description: 'Environment to deploy to')
    choice(name: 'ACTION', choices: ['build', 'test', 'deploy'], description: 'Action to perform')
    booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip tests during build')
  }
  stages {
    stage ("load script") {
      steps {
        script {
          gv = load "script.groovy"
        }
      }
    }
    
    stage ("build") {
      steps {
        script {
          gv.buildApp()
        }
      }
    }
    
    stage ("test") {
      
      when {
        expression { return !params.SKIP_TESTS }
      }
      steps {
        script {
          env.ENV = input message: "Select the env to deploy to", ok: "Done", parameters:[choice(name:'Test', choices: ['main', 'dev'])]
          gv.testApp()
        }
      }      
    }
    
    stage ("deploy") {
      input {
          message "Select to approve deployment to environment"
          ok "Approve"
          parameters {
            choice(name: 'ENV1', choices: ['dev', 'qa', 'prod'], description: 'Environment to deploy to')
            choice(name: "ENV2", choices: ['dev', 'qa', 'prod'], description: 'Environment to deploy to')
          }
        }
      steps {
        script {
          gv.deployApp(env.ENV1)
          gv.deployApp(env.ENV2)
        }
      }     
    }
  }
}
