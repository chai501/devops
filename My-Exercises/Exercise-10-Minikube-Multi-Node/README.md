# Exercise 10: Multi-node Minikube with two applications

**Goal:** Deploy a product catalog with two replicas and a shopping cart with
three replicas on a three-node Minikube cluster, distributing each
application's pods across separate nodes.

## Files

- `product_catalog.py` serves `GET /products`.
- `shopping_cart.py` serves `GET /cart` and `POST /cart`.
- `requirements.txt` pins Flask for both applications.
- `Dockerfile.product` and `Dockerfile.shopping` build the two images.
- `product_catalog_deployment.yaml` and `shopping_cart_deployment.yaml`
  define the Deployments and Services.

Both apps use port 8080 inside the container so they can run as non-root.
Required pod anti-affinity spreads replicas of each app across distinct
Kubernetes nodes. The manifests use the `default` namespace consistently.
The cart is intentionally in-memory for this lab; its contents are not
shared between replicas or retained across pod replacement.

## Start a separate three-node cluster

The commands below create the `devops-multinode` profile and do not stop or
delete another Minikube profile:

```powershell
minikube start -p devops-multinode --driver=docker --nodes=3 --cpus=2 --memory=2048
kubectl config use-context devops-multinode
kubectl get nodes -o wide
```

Confirm three nodes are `Ready`. The registry add-on is not required here:
`minikube image load` makes the locally built images available to cluster
nodes without publishing them to an external registry.

The memory setting is per node. Allocate enough memory to Docker Desktop for
the control plane, two workers, and the other running containers. On a
resource-constrained machine, temporarily stop other containers before
starting the cluster.

## Build and load both images

Run from this folder:

```powershell
docker build -f Dockerfile.product -t product-catalog:1.0 .
docker build -f Dockerfile.shopping -t shopping-cart:1.0 .
minikube -p devops-multinode image load product-catalog:1.0
minikube -p devops-multinode image load shopping-cart:1.0
```

## Deploy and verify replica placement

```powershell
kubectl --context devops-multinode apply -f product_catalog_deployment.yaml
kubectl --context devops-multinode apply -f shopping_cart_deployment.yaml
kubectl --context devops-multinode rollout status deployment/product-catalog --timeout=180s
kubectl --context devops-multinode rollout status deployment/shopping-cart --timeout=180s
kubectl --context devops-multinode get deployments
kubectl --context devops-multinode get pods -o wide
kubectl --context devops-multinode get services
```

Expected: `product-catalog` has `2/2` ready replicas and `shopping-cart` has
`3/3`. In the pod listing, replicas of each application should be assigned to
different node names.

## Test the services

In separate PowerShell terminals, forward each Service:

```powershell
kubectl --context devops-multinode port-forward service/product-catalog-service 18081:80
```

```powershell
kubectl --context devops-multinode port-forward service/shopping-cart-service 18082:80
```

In another terminal, verify the catalog and cart endpoints:

```powershell
Invoke-RestMethod http://127.0.0.1:18081/products
Invoke-RestMethod http://127.0.0.1:18082/cart
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:18082/cart -ContentType 'application/json' -Body '{"id":1,"name":"Laptop","quantity":1}'
```

The catalog returns three products. The cart starts empty and the POST returns
the submitted item. Since the cart is in-memory and there are three replicas,
the response to a later request may be served by a different replica; use a
single replica during the demo if you need to demonstrate persistent
read-after-write behavior, or add shared storage in a future exercise.

Stop the port-forward terminals with `Ctrl+C`. Keep the named Minikube profile
for future use, or stop it when finished:

```powershell
minikube -p devops-multinode stop
```

To remove only this exercise's Kubernetes resources:

```powershell
kubectl --context devops-multinode delete -f shopping_cart_deployment.yaml
kubectl --context devops-multinode delete -f product_catalog_deployment.yaml
```

**Status:** Complete. The three-node profile was brought up; all nodes reached
`Ready`; both images loaded; the catalog reached 2/2 replicas and the cart
3/3; all replicas of each app were scheduled on separate nodes. Both Service
endpoints were tested, including the catalog response and cart GET/POST.
The profile was stopped after verification to return memory to the other
exercise containers. Run the start and deploy commands above to demo it again.

**Original lab:** [Multi-Node, Multi-App Minikube Deployment](https://github.com/SunagP/DevOps-Lab/blob/main/Exercises/10-Minikube-Multi-Node-Multi-App-Minikube-Deployment.md).
