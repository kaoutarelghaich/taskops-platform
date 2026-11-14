def buildApp() {
  echo "Building the app"
  sh 'make build'
}

def testApp() {
  echo "Testing the app"
}
def buildImage() {
  echo "Building the Docker image"
  sh 'docker build -t koukidevops/taskops-api:1.0 .'
}

def pushImage() {
  withCredentials ([
      usernamePassword(
          credentialsId: 'docker-hub',
          usernameVariable: 'USER',
          passwordVariable: 'TOKEN'
      )
  ]) {
      sh 'set +x; printf "%s" "$TOKEN" | docker login -u "$USER" --password-stdin'
      sh 'docker push koukidevops/taskops-api:1.0'
  }
}

def archiveArtifacts() {
  archiveArtifacts artifacts: '**/dist/*.whl', allowEmptyArchive: true
}

def deployApp(env) {
  echo "Deploying the app to environment: ${env}"
}

return this