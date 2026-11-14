#!/usr/bin/env groovy

@Library('jenkins-shared-library') _

pipeline{

  agent any
  
  stages {
    stage ("load script") {
      steps {
        script {
          gv = load "script.groovy"
        }
      }
    }

    stage ("Archive") {
      steps {
        script {
          gv.archiveArtifacts()
        }
      }
    }

    /*
    stage ("build") {
      steps {
        script {
          buildApp()
        }
      }
    }
    */
    stage ("build images") {
      steps {
        script {
          buildImage 'koukidevops/taskops-api:1.0'
        }
      }
    }

    stage ("push image") {
      steps {
        script {
          pushImage 'koukidevops/taskops-api:1.0'
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
