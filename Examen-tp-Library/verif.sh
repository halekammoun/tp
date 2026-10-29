
#!/bin/bash

echo "======================================"
echo "       VERIFICATION DE L'EXAMEN"
echo "======================================"

echo ""
echo "========== Dockerfile Books =========="
cat books/Dockerfile

echo ""
echo "========== Dockerfile Members =========="
cat members/Dockerfile

echo ""
echo "========== Dockerfile Loans =========="
cat loans/Dockerfile

echo ""
echo "========== Dockerfile Database =========="
cat database/Dockerfile

echo ""
echo "========== Docker Containers =========="
docker ps

echo ""
echo "========== Verification completed =========="

read -r -p "Voulez-vous continuer ? (Y/N) : " answer

case "$answer" in
    Y|y|YES|yes)
        # Vérifier le dossier avant toute suppression
        exam_dir="$(pwd)"

        if [[ "$(basename "$exam_dir")" != "Examen-tp-Library" ]]; then
            echo "Erreur : lancez le script depuis le dossier Examen-tp-Library."
            exit 1
        fi

        if [[ ! -f "$exam_dir/README.md" || ! -d "$exam_dir/base-images" ]]; then
            echo "Erreur : structure du projet non reconnue."
            exit 1
        fi

        echo ""
        echo "Nettoyage Docker..."

        if ! docker system prune -a --volumes -f; then
            echo "Erreur pendant le nettoyage Docker."
            exit 1
        fi

        echo ""
        echo "Suppression du dossier de l'examen..."

        cd .. || exit 1
        rm -rf -- "$exam_dir"

        echo "Dossier de l'examen supprimé."
        ;;

    N|n|NO|no)
        echo "Opération annulée."
        exit 0
        ;;

    *)
        echo "Réponse invalide. Tapez Y ou N."
        exit 1
        ;;
esac
