import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
import hudson.security.HudsonPrivateSecurityRealm
import jenkins.model.Jenkins
import org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition
import org.jenkinsci.plugins.workflow.job.WorkflowJob

def jenkins = Jenkins.get()
def password = System.getenv("JENKINS_ADMIN_PASSWORD")
if (!password) {
    throw new IllegalStateException("JENKINS_ADMIN_PASSWORD must be set")
}

def securityRealm = new HudsonPrivateSecurityRealm(false)
if (securityRealm.getUser("admin") == null) {
    securityRealm.createAccount("admin", password)
}
jenkins.setSecurityRealm(securityRealm)

def authorizationStrategy = new FullControlOnceLoggedInAuthorizationStrategy()
authorizationStrategy.setAllowAnonymousRead(false)
jenkins.setAuthorizationStrategy(authorizationStrategy)

def projectPath = "/workspace/exercise"
def pipelineFile = new File("${projectPath}/Jenkinsfile")
if (!pipelineFile.isFile()) {
    throw new IllegalStateException("Exercise 6 Jenkinsfile not found at ${pipelineFile}")
}

def job = jenkins.getItem("Exercise6-Delivery-Pipeline")
if (job == null) {
    job = jenkins.createProject(WorkflowJob, "Exercise6-Delivery-Pipeline")
}
job.setDefinition(new CpsFlowDefinition(pipelineFile.getText("UTF-8"), true))
job.setDescription("Validates and builds the Exercise 6 delivery metrics exporter.")
job.save()
jenkins.save()
