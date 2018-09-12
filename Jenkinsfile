pipeline {
  agent none
  stages {
    stage('Create Tar') {
      steps {
        sh 'tar cf scorch.tar scorch python functions plugins/DEMO'
      }
    }
  }
}