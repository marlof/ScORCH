node {
  checkout scm
  
  stage 'test'
  sh 'echo test'
  
  stage 'package'
  sh 'tar tvf test.tar LICENSE README.md'
  
  stage 'publish'
  sh 'echo publish'
}
  
  
