node {
  checkout scm

  stage 'test'
  sh 'echo test'

  stage 'package'
  sh 'tar cf scorch.tar LICENSE README.md scorch obrar bin python functions plugins/DEMO'

//   /var/apache-maven/bin/mvn clean package
//  str_ProgramName=scorch
//  if $SNAPSHOT ; then
//    str_ProgramVersion=$RELEASE
//  else
//    str_ProgramVersion=$(grep -a "^typeset str_ProgramVersion=" ${str_ProgramName} | cut -d"=" -f2 | tr -d '"')
//  fi

//  ls -lR
//  tar cf scorch.tar ${str_ProgramName} bin obrar python functions plugins/DEMO

//  md5sum scorch.tar > scorch.tar.md5
//  cp scorch.tar      escorch.${str_ProgramVersion}.tar
//  cp scorch.tar.md5  escorch.${str_ProgramVersion}.tar.md5.txt
//  echo ${str_ProgramVersion} > version.txt

//  mv scorch.tar      latest.tar
//  mv scorch.tar.md5  latest.tar.md5
//  mv bin/install     install

  stage 'publish'
  sh 'echo publish'
}
