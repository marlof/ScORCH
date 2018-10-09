node {
  checkout scm
  
  stage 'test'
  sh 'echo test'
  
  stage 'package'
  sh 'tar cf test.tar LICENSE README.md obrar python functions plugins/DEMO'
  
  stage 'publish'
  sh 'echo publish'
}
  
  
